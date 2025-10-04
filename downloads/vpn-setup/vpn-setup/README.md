# VPN Setup with Full VM Control

**Complete solution to connect to any OpenVPN server from a Docker container without `/dev/net/tun` access.**

Works in: Docker, Cursor IDE, restricted cloud shells, any environment without kernel access.

---

## 📋 What You Need

- Docker container with internet access
- Sudo privileges inside the container
- Your OpenVPN configuration file (`.ovpn` file from your VPN provider)
- ~1GB free disk space
- ~200MB RAM

---

## 🚀 Complete Installation Guide

### Step 1: Download This Package

If you got this from gofile.io:

```bash
# Install wget if not present
sudo apt-get update && sudo apt-get install -y wget unzip

# Download from gofile (replace URL with the actual link)
wget -O vpn-setup.zip "https://gofile.io/d/XXXXXX"

# Or use curl
curl -L -o vpn-setup.zip "https://gofile.io/d/XXXXXX"
```

If you already have the file:

```bash
# Just unzip it
unzip vpn-setup.zip
cd vpn-setup
```

### Step 2: Get Your OpenVPN Config File

You need a `.ovpn` file from your VPN provider. Examples:

**For Hack The Box:**
1. Go to https://app.hackthebox.com/
2. Login to your account
3. Click on "Machines" or "Labs"
4. Click "Connect to HTB"
5. Select your lab (e.g., "Starting Point", "Machines")
6. Download the OpenVPN configuration file
7. It will be named something like `lab_username123.ovpn`

**For other VPNs:**
- Check your provider's website for OpenVPN configuration files
- Look for "Download OpenVPN config" or "Connection pack"
- Make sure it's a `.ovpn` file (not `.conf`)

### Step 3: Place Your VPN Config

**IMPORTANT:** The file MUST be named exactly `vpn.ovpn` and placed in `~/vpn-qemu/`

```bash
# Create the directory
mkdir -p ~/vpn-qemu

# Copy your .ovpn file there and rename it
cp ~/Downloads/lab_username123.ovpn ~/vpn-qemu/vpn.ovpn

# Or if it's in the current directory:
cp my-vpn-config.ovpn ~/vpn-qemu/vpn.ovpn

# Verify it's there
ls -lh ~/vpn-qemu/vpn.ovn

# You should see: -rw-r--r-- 1 user user 3.3K ... vpn.ovpn
```

**Common locations for downloaded .ovpn files:**
- `~/Downloads/`
- `~/Desktop/`
- `/tmp/`
- Current directory: `./`

### Step 4: Run VPN Setup

```bash
# Make sure you're in the vpn-setup directory
cd vpn-setup

# Run the setup script (will take 5-10 minutes first time)
bash setup-vpn.sh
```

**What this does:**
1. Installs dependencies (QEMU, cloud-init tools)
2. Downloads Debian 12 VM image (~330MB, only once)
3. Creates and starts a virtual machine
4. Installs OpenVPN and microsocks inside the VM
5. Connects to your VPN
6. Starts SOCKS5 proxy on `127.0.0.1:10080`

**Expected output at the end:**
```
=== ✅ VPN CONNECTED ✅ ===

SOCKS5 proxy available at: 127.0.0.1:10080
```

**If you see this, SUCCESS! ✅**

### Step 5: Install VM Control Wrappers

```bash
# Run the wrappers setup
bash setup-wrappers.sh

# Reload your shell environment
source ~/.bashrc
```

**What this does:**
- Creates command shortcuts: `vm`, `vm-sudo`, `vm-run`, `vm-put`, `vm-get`, `vm-check`
- Allows you to control the VM and install tools on-demand

**Verify it worked:**
```bash
# Check VPN status
vm-check

# You should see:
# - tun0 interface with an IP address
# - Routes to VPN networks
# - OpenVPN log showing "Initialization Sequence Completed"
```

---

## ✅ Verify Everything Works

Run these commands to confirm your VPN is working:

```bash
# 1. Check VPN status
vm-check

# 2. Test connectivity (replace 10.10.10.10 with your target IP)
vm 'ping -c 3 10.10.10.10'

# 3. Test SOCKS5 proxy
curl --socks5-hostname 127.0.0.1:10080 https://icanhazip.com/
```

If all three work, you're ready to go! 🎉

---

## 🔧 How to Use

### Method 1: SOCKS5 Proxy (from container)

Use the SOCKS5 proxy to route traffic through the VPN:

```bash
# Install tools in the container (not VM)
sudo apt-get install -y proxychains4 nmap curl

# Configure proxychains (one-time setup)
printf '[ProxyList]\nsocks5 127.0.0.1 10080\n' | sudo tee /etc/proxychains.conf

# Use curl through VPN
curl --socks5-hostname 127.0.0.1:10080 http://10.10.10.10/

# Use nmap through VPN (only TCP connect scan works)
proxychains4 -q nmap -sT -Pn -n -p 22,80,443,8080 10.10.10.10

# Use any tool through VPN
proxychains4 ssh user@10.10.10.10
proxychains4 python3 exploit.py
```

### Method 2: Direct VM Access (recommended for pentesting)

Execute commands directly inside the VM where the VPN is running:

#### Execute Commands

```bash
# Simple command
vm 'nmap -p- 10.10.10.10'

# With sudo
vm-sudo 'apt-get update'

# Interactive shell
vm
# (now you're inside the VM, type 'exit' to leave)
```

#### Install Tools On-Demand

```bash
# Install nmap
vm-sudo 'apt-get update && apt-get install -y nmap'

# Install gobuster
vm-sudo 'apt-get install -y gobuster'

# Install Python tools
vm-sudo 'apt-get install -y python3-pip'
vm-sudo 'pip3 install requests beautifulsoup4'

# Install multiple tools at once
vm-sudo 'apt-get install -y nmap gobuster sqlmap hydra nikto'

# Install from source
vm-sudo 'git clone https://github.com/tool/repo && cd repo && make install'
```

#### Upload and Run Scripts

```bash
# Upload a single file
vm-put exploit.py /tmp/

# Upload a folder
vm-put ./tools/ /home/cursor/tools/

# Upload and execute
vm-put exploit.py /tmp/
vm 'python3 /tmp/exploit.py 10.10.10.10'

# Execute script from stdin (runs as root)
cat <<'SCRIPT' | vm-run
apt-get update
apt-get install -y tool1 tool2
nmap -sV 10.10.10.10
SCRIPT
```

#### Download Files from VM

```bash
# Download file to current directory
vm-get /tmp/loot.txt ./

# Download to specific location
vm-get /root/flag.txt ~/flags/

# Download entire folder
vm-get /home/cursor/results/ ./
```

---

## 💡 Real-World Examples

### Example 1: Hack The Box Machine

```bash
# 1. Scan target
vm 'nmap -sC -sV -p- 10.10.11.50'

# 2. Install gobuster
vm-sudo 'apt-get update && apt-get install -y gobuster'

# 3. Web directory enumeration
vm 'gobuster dir -u http://10.10.11.50/ -w /usr/share/wordlists/dirb/common.txt'

# 4. Upload exploit
vm-put exploit.py /tmp/

# 5. Run exploit
vm 'python3 /tmp/exploit.py 10.10.11.50'

# 6. Get flag
vm-get /tmp/user.txt ./
```

### Example 2: SQLMap Test

```bash
# Install sqlmap
vm-sudo 'apt-get install -y sqlmap'

# Run sqlmap
vm 'sqlmap -u "http://10.10.10.10/page?id=1" --batch --dbs'
```

### Example 3: Hydra Bruteforce

```bash
# Install hydra
vm-sudo 'apt-get install -y hydra'

# Upload wordlists
vm-put users.txt /tmp/
vm-put passwords.txt /tmp/

# Run bruteforce
vm 'hydra -L /tmp/users.txt -P /tmp/passwords.txt ssh://10.10.10.10'
```

### Example 4: Multi-Step Attack

```bash
# Create attack script
cat > attack.sh <<'SCRIPT'
#!/bin/bash
set -e

# Install tools
apt-get update
apt-get install -y nmap gobuster nikto

# Scan
echo "[*] Scanning target..."
nmap -sV -p- 10.10.10.10 -oN /tmp/nmap.txt

# Web enum
echo "[*] Enumerating web dirs..."
gobuster dir -u http://10.10.10.10/ -w /usr/share/wordlists/dirb/common.txt -o /tmp/gobuster.txt

# Nikto scan
echo "[*] Running nikto..."
nikto -h http://10.10.10.10/ -o /tmp/nikto.txt

echo "[*] Done! Results in /tmp/"
SCRIPT

# Upload and execute
cat attack.sh | vm-run

# Download all results
vm-get /tmp/nmap.txt ./
vm-get /tmp/gobuster.txt ./
vm-get /tmp/nikto.txt ./
```

---

## 🔍 Troubleshooting

### Issue: "SSH not available"

**Cause:** VM is still booting (takes 1-3 minutes)

**Solution:**
```bash
# Wait and check console log
tail -f ~/vpn-qemu/guest-console.log

# Look for: "Started OpenBSD Secure Shell server"
# Once you see it, try again
```

### Issue: "tun0 not up" / VPN not connecting

**Cause:** Invalid .ovpn file or wrong credentials

**Solution:**
```bash
# Check OpenVPN log inside VM
vm-sudo 'tail -n 100 /var/log/openvpn.log'

# Look for errors like:
# - "AUTH_FAILED" = wrong credentials
# - "Connection refused" = wrong server
# - "TLS handshake failed" = certificate issue

# Make sure your .ovpn file is correct and complete
cat ~/vpn-qemu/vpn.ovpn | head -20
```

### Issue: "Cannot connect to target IP"

**Cause:** VPN connected but routes not working

**Solution:**
```bash
# Check if tun0 is up
vm 'ip a show tun0'
# Should show: tun0 with IP like 10.10.14.50/23

# Check routes
vm 'ip r | grep 10.'
# Should show routes to VPN networks

# Test gateway
vm 'ping -c 3 10.10.14.1'
# Should get replies

# If gateway works but target doesn't:
# - Target might be down/offline
# - Firewall blocking
# - Wrong IP address
```

### Issue: "SOCKS5 connection failed"

**Cause:** microsocks not running or crashed

**Solution:**
```bash
# Check if microsocks is running
vm-sudo 'ss -lntp | grep 1080'
# Should show: microsocks on 0.0.0.0:1080

# If not, restart it
vm-sudo 'pkill microsocks'
vm-sudo 'nohup microsocks -i 0.0.0.0 -p 1080 > /var/log/microsocks.log 2>&1 &'

# Test SOCKS5
curl --socks5-hostname 127.0.0.1:10080 https://icanhazip.com/
```

### Issue: Command not found: vm, vm-sudo, etc.

**Cause:** PATH not updated in current shell

**Solution:**
```bash
# Reload shell environment
source ~/.bashrc

# Or use full path
~/.local/bin/vm 'whoami'

# Or restart your terminal session
```

### Issue: Very slow connection

**Cause:** High latency to VPN server or network congestion

**Solution:**
```bash
# Check latency
vm 'ping -c 10 8.8.8.8'

# If >500ms average:
# - Try different VPN server (get new .ovpn)
# - Check your internet connection
# - VPN server might be overloaded
```

---

## 🔄 Common Operations

### Restart VPN Connection

```bash
# Kill VM
killall -9 qemu-system-x86_64

# Start again
cd vpn-setup
bash setup-vpn.sh
```

### Connect to Different VPN

```bash
# Stop current VM
killall -9 qemu-system-x86_64

# Replace config
cp ~/Downloads/new-vpn.ovpn ~/vpn-qemu/vpn.ovpn

# Restart
cd vpn-setup
bash setup-vpn.sh
```

### Check What's Running

```bash
# Check QEMU process
pgrep -a qemu

# Check ports
ss -tlnp | grep 10022  # SSH to VM
ss -tlnp | grep 10080  # SOCKS5 proxy

# Check from inside VM
vm-check
```

### Access VM Directly (for debugging)

```bash
# SSH into VM
sshpass -p cursor ssh -p 10022 cursor@127.0.0.1

# Inside VM:
whoami         # cursor
sudo -i        # become root
ip a show tun0 # check VPN interface
tail -f /var/log/openvpn.log  # watch logs
```

### Clean Up Everything

```bash
# Kill VM
killall -9 qemu-system-x86_64

# Remove files (CAREFUL: deletes VPN config too!)
rm -rf ~/vpn-qemu/

# Remove wrappers
rm -f ~/.local/bin/vm*

# Remove PATH modification (optional)
sed -i '/\.local\/bin/d' ~/.bashrc
```

---

## 📊 Technical Details

**VM Specifications:**
- OS: Debian 12 (Bookworm)
- RAM: 1792 MB
- CPUs: 2 cores
- Disk: ~1GB (qcow2 format)
- Network: User-mode networking (no root required)

**Installed Services:**
- OpenVPN: Connects to VPN server
- microsocks: SOCKS5 proxy (no authentication)
- SSH: Remote access (user: cursor, pass: cursor)

**Port Forwards:**
- `127.0.0.1:10022` → VM:22 (SSH)
- `127.0.0.1:10080` → VM:1080 (SOCKS5)

**Performance:**
- Latency overhead: +5-10ms
- Throughput: ~80-90% of native VPN
- Idle RAM: ~200MB
- Idle CPU: <1%

---

## ⚠️ Important Notes

### SOCKS5 Limitations

❌ **Won't work:**
- ICMP (ping) - `ping` command won't work through SOCKS5
- UDP traffic (some VPNs)
- SYN scans with nmap (`-sS`)

✅ **Will work:**
- TCP connections
- HTTP/HTTPS
- SSH
- TCP connect scans (`-sT`)
- Most tools with proxychains

### Security Notes

- VM has full internet access - be careful what you run
- SSH password is hardcoded (cursor:cursor) - only localhost access
- No firewall between container and VM
- SOCKS5 has no authentication (only bound to localhost)

### Known Issues

- First boot takes 5-10 minutes (downloads 330MB image)
- Subsequent boots take 1-2 minutes
- Zombie processes normal (cleaned up automatically)
- Locale warnings harmless (can be ignored)

---

## 🆘 Still Having Issues?

1. Check VM console log:
   ```bash
   tail -n 200 ~/vpn-qemu/guest-console.log
   ```

2. Check OpenVPN log:
   ```bash
   vm-sudo 'cat /var/log/openvpn.log'
   ```

3. Test basic connectivity:
   ```bash
   vm 'ping -c 3 8.8.8.8'
   ```

4. Verify SSH working:
   ```bash
   nc -zv 127.0.0.1 10022
   ```

5. Check if QEMU is running:
   ```bash
   pgrep -a qemu
   ```

---

## 📚 Additional Resources

- [OpenVPN Documentation](https://openvpn.net/community-resources/)
- [QEMU Documentation](https://www.qemu.org/docs/master/)
- [microsocks GitHub](https://github.com/rofl0r/microsocks)
- [proxychains Documentation](https://github.com/haad/proxychains)

---

## 📄 Credits

Created for containerized environments without kernel access (Docker, Cursor IDE, restricted cloud shells).

Solution uses QEMU for VM virtualization, Debian for guest OS, OpenVPN for VPN connectivity, and microsocks for SOCKS5 proxy.

---

**Enjoy your VPN access! 🚀**
