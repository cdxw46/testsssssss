#!/usr/bin/env bash
set -euxo pipefail
if ! command -v modprobe >/dev/null 2>&1; then
  apt-get update -y && apt-get install -y kmod
fi
modprobe tun || true
mkdir -p /dev/net
[ -e /dev/net/tun ] || (mknod /dev/net/tun c 10 200 && chmod 0666 /dev/net/tun)
install -D -m 0644 /home/cursor/vpn.ovpn /etc/openvpn/vpn.conf
if [ -f /run/openvpn.pid ]; then
  pkill -F /run/openvpn.pid || true
fi
pkill -f "openvpn --config /etc/openvpn/vpn.conf" || true
sleep 1
nohup openvpn --config /etc/openvpn/vpn.conf --daemon --writepid /run/openvpn.pid --log /var/log/openvpn.log
for i in $(seq 1 60); do
  ip a show tun0 >/dev/null 2>&1 && break || sleep 2
done
ip -brief a
ip r
 tail -n 80 /var/log/openvpn.log || true
