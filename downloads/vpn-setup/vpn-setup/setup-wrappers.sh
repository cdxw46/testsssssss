#!/bin/bash
# === VM CONTROL WRAPPERS (dinámico, sin herramientas preinstaladas) ===
# Crea wrappers para control total de la VM desde el contenedor

set -Eeuo pipefail

# 0) Dependencias mínimas en el contenedor
sudo apt-get update -y > /dev/null 2>&1
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y sshpass rsync netcat-openbsd curl > /dev/null 2>&1

# 1) Parámetros de la VM
VM_HOST="127.0.0.1"
SSH_PORT="10022"
VM_USER="cursor"
VM_PASS="cursor"

# 2) Verificar SSH
echo "[*] Checking SSH on ${VM_HOST}:${SSH_PORT}..."
for i in $(seq 1 30); do
  nc -z "${VM_HOST}" "${SSH_PORT}" 2>/dev/null && { echo "✓ SSH available"; break; } || true
  sleep 2
done
nc -z "${VM_HOST}" "${SSH_PORT}" || { echo "ERROR: SSH not available. Run setup-vpn.sh first."; exit 1; }

# 3) Crear wrappers
BIN="$HOME/.local/bin"
mkdir -p "$BIN"

# vm: ejecuta comando en la VM
cat > "$BIN/vm" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
VM_HOST="${VM_HOST:-127.0.0.1}"
SSH_PORT="${SSH_PORT:-10022}"
VM_USER="${VM_USER:-cursor}"
VM_PASS="${VM_PASS:-cursor}"
if [ $# -eq 0 ]; then
  exec sshpass -p "$VM_PASS" ssh -t -p "$SSH_PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$VM_USER@$VM_HOST" "bash -l"
else
  sshpass -p "$VM_PASS" ssh -p "$SSH_PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$VM_USER@$VM_HOST" "bash -lc \"$*\""
fi
EOF
chmod +x "$BIN/vm"

# vm-sudo: ejecuta con sudo
cat > "$BIN/vm-sudo" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
VM_HOST="${VM_HOST:-127.0.0.1}"
SSH_PORT="${SSH_PORT:-10022}"
VM_USER="${VM_USER:-cursor}"
VM_PASS="${VM_PASS:-cursor}"
if [ $# -eq 0 ]; then
  exec sshpass -p "$VM_PASS" ssh -t -p "$SSH_PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$VM_USER@$VM_HOST" "sudo bash -l"
else
  sshpass -p "$VM_PASS" ssh -p "$SSH_PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$VM_USER@$VM_HOST" "sudo bash -lc \"$*\""
fi
EOF
chmod +x "$BIN/vm-sudo"

# vm-run: lee script de STDIN
cat > "$BIN/vm-run" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
VM_HOST="${VM_HOST:-127.0.0.1}"
SSH_PORT="${SSH_PORT:-10022}"
VM_USER="${VM_USER:-cursor}"
VM_PASS="${VM_PASS:-cursor}"
exec sshpass -p "$VM_PASS" ssh -p "$SSH_PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$VM_USER@$VM_HOST" 'sudo bash -se' < /dev/stdin
EOF
chmod +x "$BIN/vm-run"

# vm-put: subir archivos
cat > "$BIN/vm-put" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 1 ]; then echo "uso: vm-put <archivo|carpeta> [destino_en_VM]"; exit 1; fi
SRC="$1"; DST="${2:-/home/cursor/}"
VM_HOST="${VM_HOST:-127.0.0.1}"
SSH_PORT="${SSH_PORT:-10022}"
VM_USER="${VM_USER:-cursor}"
VM_PASS="${VM_PASS:-cursor}"
if [ -d "$SRC" ]; then
  sshpass -p "$VM_PASS" rsync -avz -e "ssh -p $SSH_PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" "$SRC" "$VM_USER@$VM_HOST:$DST"
else
  sshpass -p "$VM_PASS" scp -P "$SSH_PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$SRC" "$VM_USER@$VM_HOST:$DST"
fi
EOF
chmod +x "$BIN/vm-put"

# vm-get: descargar desde VM
cat > "$BIN/vm-get" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 1 ]; then echo "uso: vm-get <ruta_en_VM> [destino_local]"; exit 1; fi
SRC="$1"; DST="${2:-.}"
VM_HOST="${VM_HOST:-127.0.0.1}"
SSH_PORT="${SSH_PORT:-10022}"
VM_USER="${VM_USER:-cursor}"
VM_PASS="${VM_PASS:-cursor}"
sshpass -p "$VM_PASS" scp -P "$SSH_PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$VM_USER@$VM_HOST:$SRC" "$DST"
EOF
chmod +x "$BIN/vm-get"

# vm-check: estado VPN
cat > "$BIN/vm-check" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
VM_HOST="${VM_HOST:-127.0.0.1}"
SSH_PORT="${SSH_PORT:-10022}"
VM_USER="${VM_USER:-cursor}"
VM_PASS="${VM_PASS:-cursor}"
sshpass -p "$VM_PASS" ssh -p "$SSH_PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$VM_USER@$VM_HOST" '
  echo "=== IFACES ==="; ip -brief a || true
  echo "=== ROUTES ==="; ip r || true
  echo "=== OPENVPN LOG TAIL ==="; sudo tail -n 60 /var/log/openvpn.log 2>/dev/null || sudo tail -n 60 /var/log/openvpn-htb.log 2>/dev/null || echo "No openvpn log found"
'
EOF
chmod +x "$BIN/vm-check"

# 4) Añadir al PATH
if ! grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

echo ""
echo "=== ✅ WRAPPERS INSTALLED ✅ ==="
echo ""
echo "Available commands:"
echo "  vm          - Execute command in VM"
echo "  vm-sudo     - Execute command with sudo"
echo "  vm-run      - Execute script from stdin (as root)"
echo "  vm-put      - Upload files/folders to VM"
echo "  vm-get      - Download files from VM"
echo "  vm-check    - Check VPN status and routes"
echo ""
echo "Examples:"
echo "  vm 'nmap -sV TARGET_IP'"
echo "  vm-sudo 'apt-get update && apt-get install -y sqlmap'"
echo "  vm-put exploit.py /tmp/ && vm 'python3 /tmp/exploit.py'"
echo "  cat script.sh | vm-run"
echo "  vm-check"
echo ""
echo "⚠️  Run: source ~/.bashrc  (to update PATH in current shell)"
