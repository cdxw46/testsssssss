#!/usr/bin/env bash
set -euo pipefail
exec timeout 180s ~/.local/bin/mssqlclient.py -windows-auth -target-ip 10.129.116.248 DARKZERO.HTB/john.w:RFulUtONCOL!@10.129.116.248 -show -file /home/cursor/msdb_roles.sql
