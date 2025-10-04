#!/usr/bin/env bash
set -euxo pipefail
export DEBIAN_FRONTEND=noninteractive
if ! command -v modprobe >/dev/null 2>&1; then
  apt-get update -y
  apt-get install -y kmod
fi
modprobe tun || true
mkdir -p /dev/net
[ -e /dev/net/tun ] || (mknod /dev/net/tun c 10 200 && chmod 0666 /dev/net/tun)
# Ensure OpenVPN config is in place
if [ -f /home/cursor/vpn.ovpn ]; then
  install -D -m 0644 /home/cursor/vpn.ovpn /etc/openvpn/vpn.conf
fi
# Start OpenVPN as daemon with log
nohup openvpn --config /etc/openvpn/vpn.conf --daemon --writepid /run/openvpn.pid --log /var/log/openvpn.log
# Wait for tun0 to appear
for i in $(seq 1 90); do
  ip a show tun0 >/dev/null 2>&1 && break || sleep 2
done
ip a show tun0 >/dev/null 2>&1 || { echo "[FAIL] tun0 not up"; tail -n 200 /var/log/openvpn.log || true; exit 1; }
# Start SOCKS5 proxy on 0.0.0.0:1080
nohup microsocks -i 0.0.0.0 -p 1080 > /var/log/microsocks.log 2>&1 &
sleep 2
# Verification outputs
ss -lntp | grep 1080 || { echo "[FAIL] microsocks not listening"; exit 1; }
ip -brief a || true
ip r || true
