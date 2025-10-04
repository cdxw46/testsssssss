#!/usr/bin/env bash
set -euxo pipefail
install -D -m 0644 /home/cursor/vpn.ovpn /etc/openvpn/vpn.conf
pkill -f openvpn || true
sleep 1
nohup openvpn --config /etc/openvpn/vpn.conf --daemon --writepid /run/openvpn.pid --log /var/log/openvpn.log
for i in $(seq 1 60); do
  ip a show tun0 >/dev/null 2>&1 && break || sleep 2
done
ip -brief a
ip r
tail -n 80 /var/log/openvpn.log || true
