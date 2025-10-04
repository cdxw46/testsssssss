#!/bin/bash
# === VPN SETUP IN DOCKER CONTAINER (NO TUN/TAP REQUIRED) ===
# Uses QEMU VM to run OpenVPN and exposes SOCKS5 proxy

set -Eeuo pipefail

echo "[0] Installing dependencies in container..."
sudo apt-get update -y
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  qemu-system-x86 qemu-utils cloud-image-utils curl ca-certificates xz-utils \
  genisoimage jq openssh-client sshpass netcat-openbsd rsync

WORK="$HOME/vpn-qemu"; mkdir -p "$WORK"; cd "$WORK"

# Download Debian 12 cloud image
IMG_URL="https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-amd64.qcow2"
IMG="$WORK/debian-12-genericcloud-amd64.qcow2"
[ -s "$IMG" ] || curl -fL "$IMG_URL" -o "$IMG"

# Check for VPN config
OVPN="$WORK/vpn.ovpn"
if [ ! -s "$OVPN" ]; then
  echo ">>> ERROR: Place your .ovpn file at $WORK/vpn.ovpn"
  exit 1
fi

echo "[1] Creating cloud-init seed for SSH access..."
cat > "$WORK/user-data" <<'EOF'
#cloud-config
hostname: vpn-guest
users:
  - name: cursor
    gecos: Cursor
    groups: [ sudo ]
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
chpasswd:
  list: |
    cursor:cursor
  expire: False
ssh_pwauth: true
write_files:
  - path: /etc/ssh/sshd_config.d/99-pw.conf
    owner: root:root
    permissions: '0644'
    content: |
      PasswordAuthentication yes
runcmd:
  - systemctl restart ssh || true
output:
  all: '| tee -a /var/log/cloud-init-output.log /dev/console'
EOF
echo "instance-id: iid-vpn-debian" > "$WORK/meta-data"
SEED="$WORK/seed.iso"
cloud-localds "$SEED" "$WORK/user-data" "$WORK/meta-data"

echo "[2] Launching QEMU VM with port forwards (SSH:10022, SOCKS:10080)..."
DISK="$WORK/disk.qcow2"
pgrep -f "qemu-system-x86_64.*$DISK" >/dev/null && kill $(pgrep -f "qemu-system-x86_64.*$DISK") || true
sleep 2
cp -f "$IMG" "$DISK"
LOG="$WORK/guest-console.log"
qemu-system-x86_64 \
  -m 1792 -smp 2 \
  -drive file="$DISK",if=virtio,format=qcow2,cache=writeback \
  -cdrom "$SEED" \
  -nic user,model=virtio-net-pci,hostfwd=tcp:127.0.0.1:10022-:22,hostfwd=tcp:127.0.0.1:10080-:1080 \
  -nographic -no-reboot \
  > "$LOG" 2>&1 &

echo "[3] Waiting for SSH on 127.0.0.1:10022..."
for i in $(seq 1 90); do
  nc -w 1 -z 127.0.0.1 10022 2>/dev/null && { echo "SSH available"; break; } || true
  sleep 2
done
nc -w 1 -z 127.0.0.1 10022 2>/dev/null || { echo "ERROR: SSH not available. Check $LOG"; exit 1; }

SSH="sshpass -p cursor ssh -p 10022 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null cursor@127.0.0.1"
SCP="sshpass -p cursor scp -P 10022 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

echo "[4] Installing OpenVPN and microsocks in VM..."
$SSH 'sudo bash -lc "
  set -euxo pipefail
  export DEBIAN_FRONTEND=noninteractive
  retry(){ n=0; until \"\$@\"; do n=\$((n+1)); [ \$n -ge 8 ] && return 1; sleep 4; done; }
  retry apt-get update
  retry apt-get install -y --no-install-recommends ca-certificates iproute2 iputils-ping curl openvpn microsocks nmap
  modprobe tun || true
  mkdir -p /dev/net
  [ -e /dev/net/tun ] || (mknod /dev/net/tun c 10 200 && chmod 0666 /dev/net/tun)
"'

echo "[5] Copying VPN config to VM and starting OpenVPN..."
$SCP "$OVPN" cursor@127.0.0.1:/home/cursor/vpn.ovpn
$SSH 'sudo bash -lc "
  set -euxo pipefail
  mv /home/cursor/vpn.ovpn /etc/openvpn/vpn.conf
  nohup openvpn --config /etc/openvpn/vpn.conf --daemon --writepid /run/openvpn.pid --log /var/log/openvpn.log
  for i in \$(seq 1 90); do ip a show tun0 && break || sleep 2; done
  ip a show tun0 || (echo \"[FAIL] tun0 not up\"; tail -n 200 /var/log/openvpn.log || true; exit 1)
  ip r || true
"'

echo "[6] Starting SOCKS5 proxy (microsocks) in VM on 0.0.0.0:1080..."
$SSH 'sudo bash -lc "
  nohup microsocks -i 0.0.0.0 -p 1080 > /var/log/microsocks.log 2>&1 &
  sleep 2
  ss -lntp | grep 1080 || (echo \"[FAIL] microsocks not listening\"; exit 1)
"'

echo ""
echo "=== ✅ VPN CONNECTED ✅ ==="
echo ""
echo "SOCKS5 proxy available at: 127.0.0.1:10080"
echo ""
echo "Usage from container:"
echo "  curl --socks5-hostname 127.0.0.1:10080 http://TARGET_IP/"
echo ""
echo "  sudo apt-get install -y proxychains4 nmap"
echo "  printf '[ProxyList]\\nsocks5 127.0.0.1 10080\\n' | sudo tee /etc/proxychains.conf"
echo "  proxychains4 -q nmap -sT -Pn -n -p 22,80,443 TARGET_IP"
echo ""
echo "SSH to VM (for debugging):"
echo "  sshpass -p cursor ssh -p 10022 cursor@127.0.0.1"
echo ""
echo "QEMU running in background (PID: $(pgrep -f 'qemu.*disk.qcow2'))"
echo ""
echo "Next step: Run setup-wrappers.sh for full VM control"
