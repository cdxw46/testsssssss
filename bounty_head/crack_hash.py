#!/usr/bin/env python3
from passlib.hash import sha512_crypt
import sys

hash_str = "$6$iUTv82apTZ0MdMP3$a+hjcpVv7OkX7pYipIPjFqisGfxLegS7FmRiLcOJBF3uaIwdMKpuQvVh0nTpglaUBsn18pssy2ZFvWlZleT8Fg"

# Intentar con contraseñas comunes primero
common_passwords = [
    "password", "admin", "root", "12345", "123456", "1234567", "12345678",
    "bounty", "cyborg", "dominic", "f35426", "mqbox", "mqtt", 
    "Cu$t0mB00Tl04d3r", "custom", "bootloader",
    "tplink", "tp-link", "TP-LINK", "TPLink"
]

for password in common_passwords:
    if sha512_crypt.verify(password, hash_str):
        print(f"FOUND: {password}")
        sys.exit(0)

# Ahora intentar con rockyou.txt (primeros 50000)
try:
    with open('/tmp/rockyou.txt', 'r', encoding='latin-1') as f:
        for i, line in enumerate(f):
            if i > 50000:
                break
            password = line.strip()
            if sha512_crypt.verify(password, hash_str):
                print(f"FOUND: {password}")
                sys.exit(0)
            if i % 1000 == 0:
                print(f"Intentado {i} passwords...", file=sys.stderr)
except FileNotFoundError:
    print("No se encontró rockyou.txt", file=sys.stderr)

print("No se encontró la contraseña", file=sys.stderr)
