#!/usr/bin/env python3

from pwn import *

context.log_level = 'warn'

io = remote('94.237.57.155', 53014, timeout=5)

def cmd(option):
    io.recvuntil(b'> ', timeout=2)
    io.sendline(str(option).encode())

# Get flag
cmd(3)
io.recvuntil(b"flag:\n", timeout=2)
data = io.recvline(timeout=2).strip()
n, e, c = eval(data)

print(f"n={n.bit_length()}bits e={e}")

# Generate primes and check
for i in range(100):
    cmd(1)
    io.recvuntil(b"primes!\n", timeout=2)
    p = int(io.recvline(timeout=2))
    
    if n % p == 0:
        print(f"\nFOUND! i={i}")
        print(f"p={p}")
        print(f"q={n//p}")
        
        # Decrypt RSA
        from Crypto.Util.number import long_to_bytes
        phi = (p-1) * (n//p - 1)
        d = pow(e, -1, phi)
        m = pow(c, d, n)
        enc = long_to_bytes(m)
        print(f"AES_enc={enc.hex()}")
        
        with open('/tmp/data.txt', 'w') as f:
            f.write(f"p={p}\nq={n//p}\nenc={enc.hex()}\n")
        break
    
    if i % 20 == 0:
        print(f"{i}...")

io.close()
