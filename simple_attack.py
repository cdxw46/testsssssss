#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import long_to_bytes

io = remote('94.237.57.155', 53014)
io.timeout = 3

# Get n,e,c
io.sendlineafter(b'> ', b'3')
line = io.recvline()  # "Encrypted flag:"
n,e,c = eval(io.recvline())

print(f"[+] n={n.bit_length()}bits")

# Try primes
for i in range(80):
    io.sendlineafter(b'> ', b'1')
    io.recvline()  # "It's raining primes!"
    p = int(io.recvline())
    
    if n % p == 0:
        print(f"\n[+] FOUND at i={i}!")
        phi = (p-1)*((n//p)-1)
        d = pow(e,-1,phi)
        enc = long_to_bytes(pow(c,d,n))
        print(f"[+] AES_encrypted: {enc.hex()}")
        open('/workspace/aes_enc.bin','wb').write(enc)
        break
    
    if i%10==0: print(f"  {i}...")

io.close()
