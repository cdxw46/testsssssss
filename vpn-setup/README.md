# VPN Setup with Full VM Control (No TUN/TAP Required)

Complete solution to connect to any OpenVPN server from a Docker container without `/dev/net/tun` access or `CAP_NET_ADMIN` capabilities, plus full control wrappers for the VM.

## 🎯 What This Does

1. **VPN Connection via QEMU VM**
   - Runs Debian 12 VM in user-space using QEMU
   - OpenVPN runs inside the VM (with its own kernel and TUN support)
   - Exposes SOCKS5 proxy on `127.0.0.1:10080` in your container
   - SSH access to VM on `127.0.0.1:10022`

2. **VM Control Wrappers**
   - Execute commands in the VM on-demand
   - Install tools dynamically (no need to pre-install)
   - Upload/download files bidirectionally
   - Check VPN status and connectivity

## 📋 Requirements

- Docker container with internet access
- Sudo privileges in the container
- Your OpenVPN configuration file (.ovpn)
- ~1GB disk space + ~200MB RAM for VM

## 🚀 Quick Start

### Step 1: Extract Package

```bash
unzip vpn-setup.zip
cd vpn-setup
```

### Step 2: Place Your VPN Config

```bash
mkdir -p ~/vpn-qemu
cp /path/to/your/config.ovpn ~/vpn-qemu/vpn.ovpn
```

**Important:** File MUST be named `vpn.ovpn` and placed in `~/vpn-qemu/`

### Step 3: Setup VPN

```bash
bash setup-vpn.sh
```

This will:
- Install dependencies (QEMU, cloud-init tools)
- Download Debian 12 cloud image (~330MB, first time only)
- Create and launch VM
- Install OpenVPN and microsocks
- Connect to your VPN
- Start SOCKS5 proxy on `127.0.0.1:10080`

**Time:** ~5-10 minutes first run, ~2-3 minutes subsequent runs

### Step 4: Setup VM Control Wrappers

```bash
bash setup-wrappers.sh
source ~/.bashrc
```

This creates command wrappers for full VM control.

## 🔧 Usage

### VPN Access (SOCKS5 Proxy)

#### With curl
```bash
curl --socks5-hostname 127.0.0.1:10080 http://TARGET_IP/
```

#### With nmap (via proxychains)
```bash
# Configure proxychains (one time)
sudo apt-get install -y proxychains4 nmap
printf '[ProxyList]\nsocks5 127.0.0.1 10080\n' | sudo tee /etc/proxychains.conf

# Scan through VPN
proxychains4 -q nmap -sT -Pn -n -p 22,80,443 TARGET_IP
```

#### With other tools
```bash
proxychains4 ssh user@TARGET_IP
proxychains4 msfconsole
proxychains4 python3 exploit.py
```

### VM Control (Direct Access)

#### Execute Commands

```bash
# Simple command
vm 'uname -a'

# With sudo
vm-sudo 'apt-get update && apt-get install -y nmap'

# Interactive shell
vm  # no arguments opens shell
```

#### Install Tools On-Demand

```bash
# Install gobuster
vm-sudo 'apt-get update && apt-get install -y gobuster'

# Install Python packages
vm-sudo 'apt-get install -y python3-pip && pip3 install requests'

# Compile from source
vm-sudo 'git clone REPO && cd REPO && make && make install'
```

#### Run Scripts

```bash
# Upload and execute
vm-put exploit.py /tmp/
vm 'python3 /tmp/exploit.py'

# Execute from stdin (runs as root)
cat script.sh | vm-run

# Multi-line script
vm-run <<'SCRIPT'
apt-get update
apt-get install -y tool1 tool2
nmap -sV TARGET_IP
SCRIPT
```

#### File Transfer

```bash
# Upload file
vm-put exploit.py /tmp/

# Upload folder
vm-put ./tools/ /home/cursor/tools/

# Download file
vm-get /tmp/loot.txt ./

# Download to specific location
vm-get /root/flag.txt ./flags/
```

#### Check VPN Status

```bash
vm-check
# Shows:
# - Network interfaces (tun0)
# - Routes to target networks
# - OpenVPN log tail
```

## 💡 Real-World Pentesting Examples

### Example 1: Port Scanning

```bash
# Quick scan
vm 'nmap -p- --min-rate 5000 10.10.10.10'

# Service detection
vm 'nmap -sV -sC -p 22,80,443 10.10.10.10'
```

### Example 2: Web Enumeration

```bash
# Install gobuster
vm-sudo 'apt-get update && apt-get install -y gobuster'

# Upload wordlist
vm-put /usr/share/wordlists/dirb/common.txt /tmp/

# Run enumeration
vm 'gobuster dir -u http://10.10.10.10/ -w /tmp/common.txt'
```

### Example 3: Exploitation

```bash
# Upload exploit
vm-put exploit.py /tmp/

# Run exploit
vm 'python3 /tmp/exploit.py 10.10.10.10 4444'

# Get reverse shell output
vm-get /tmp/shell.log ./
```

### Example 4: Credential Testing

```bash
# Install hydra
vm-sudo 'apt-get install -y hydra'

# Upload user/pass lists
vm-put users.txt /tmp/
vm-put passwords.txt /tmp/

# Run bruteforce
vm 'hydra -L /tmp/users.txt -P /tmp/passwords.txt ssh://10.10.10.10'
```

## 🔍 Troubleshooting

### Check VM is Running

```bash
pgrep -a qemu
# Should show: qemu-system-x86_64 ... disk.qcow2
```

### Check VPN Connection

```bash
vm-check
# Look for: tun0 interface with IP
```

### Check SOCKS5 Proxy

```bash
curl --socks5-hostname 127.0.0.1:10080 https://icanhazip.com/
# Should return your VPN's public IP
```

### Access VM Directly

```bash
sshpass -p cursor ssh -p 10022 cursor@127.0.0.1

# Inside VM:
ip a show tun0
tail -n 100 /var/log/openvpn.log
ss -lntp | grep 1080
```

### View Console Logs

```bash
tail -n 100 ~/vpn-qemu/guest-console.log
```

### Restart Everything

```bash
# Kill VM
killall qemu-system-x86_64

# Restart
cd vpn-setup
bash setup-vpn.sh
bash setup-wrappers.sh
```

### Connect to Different VPN

```bash
# Stop current
killall qemu-system-x86_64

# Replace config
cp /path/to/new.ovpn ~/vpn-qemu/vpn.ovpn

# Restart
bash setup-vpn.sh
```

## 📊 Technical Details

### VM Specifications
- **OS:** Debian 12 (Bookworm)
- **RAM:** 1792 MB
- **CPUs:** 2 cores
- **Disk:** ~1GB (qcow2)
- **Network:** User-mode networking (no root required)

### Services
- **OpenVPN:** Connects to your VPN server
- **microsocks:** SOCKS5 proxy (no authentication)
- **SSH:** Remote access (cursor:cursor)

### Port Forwards (Container → VM)
- `127.0.0.1:10022` → VM:22 (SSH)
- `127.0.0.1:10080` → VM:1080 (SOCKS5)

### Wrappers Location
- Installed in: `~/.local/bin/`
- Commands: `vm`, `vm-sudo`, `vm-run`, `vm-put`, `vm-get`, `vm-check`

## ⚠️ Important Notes

### SOCKS5 Limitations
- **ICMP:** Ping won't work through SOCKS5
- **UDP:** Limited support (use TCP when possible)
- **nmap:** Use `-sT` (TCP connect) instead of SYN scan
- **DNS:** Use IPs or `--socks5-hostname` flag

### Performance
- **Latency:** +5-10ms overhead from VM
- **Speed:** ~80-90% of native VPN speed
- **Resources:** ~200MB RAM, negligible CPU when idle

### Security
- VM has full internet access (be careful what you run)
- SSH password is hardcoded (cursor:cursor) - only accessible on localhost
- No firewall between container and VM
- SOCKS5 has no authentication

## 🆘 Common Issues

### "SSH not available"
- VM might still be booting (wait 2-3 minutes)
- Check: `tail ~/vpn-qemu/guest-console.log`
- Restart: `killall qemu-system-x86_64 && bash setup-vpn.sh`

### "tun0 not up"
- VPN credentials might be wrong
- Check: `vm-sudo 'tail -n 100 /var/log/openvpn.log'`
- Verify .ovpn file is valid

### "SOCKS5 connection failed"
- Check microsocks: `vm-sudo 'ss -lntp | grep 1080'`
- Restart: `vm-sudo 'pkill microsocks && microsocks -i 0.0.0.0 -p 1080 &'`

### "Cannot connect to host 10.x.x.x"
- Verify VPN is connected: `vm-check`
- Check routes: `vm 'ip r | grep 10.'`
- Test from VM directly: `vm 'ping TARGET_IP'`

### Wrappers not found
- Run: `source ~/.bashrc`
- Or use full path: `~/.local/bin/vm 'command'`

## 📚 Additional Resources

- [OpenVPN Documentation](https://openvpn.net/community-resources/)
- [QEMU User Networking](https://wiki.qemu.org/Documentation/Networking#User_Networking_%28SLIRP%29)
- [microsocks GitHub](https://github.com/rofl0r/microsocks)
- [proxychains Documentation](https://github.com/haad/proxychains)

## 💬 Support

If you encounter issues:
1. Check VM console log: `~/vpn-qemu/guest-console.log`
2. Check OpenVPN log: `vm-sudo 'cat /var/log/openvpn.log'`
3. Test basic connectivity: `vm 'ping 8.8.8.8'`
4. Verify SSH: `nc -zv 127.0.0.1 10022`

## 📄 License

This setup script is provided as-is for educational and testing purposes.

---

**Created for containerized environments without kernel access (Docker, Cursor IDE, restricted cloud shells)**
