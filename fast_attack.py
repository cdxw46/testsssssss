#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import long_to_bytes

io = remote('94.237.57.155', 53014, timeout=3)

# Get n,e,c
io.recv(timeout=2)
io.sendline(b'3')
io.recvuntil(b'flag:\n')
n,e,c = eval(io.recvline())

print(f"[+] n={n.bit_length()} bits")

# Try primes
for i in range(80):
    io.recvuntil(b'> ')
    io.sendline(b'1')
    io.recvuntil(b'primes!\n')
    p = int(io.recvline())
    
    if n % p == 0:
        q = n // p
        print(f"[+] FOUND! p={p.bit_length()}bits")
        
        phi = (p-1)*(q-1)
        d = pow(e,-1,phi)
        m = pow(c,d,n)
        enc = long_to_bytes(m)
        print(f"[+] RSA dec: {enc.hex()}")
        
        # Save
        open('/workspace/rsa_dec.txt','w').write(enc.hex())
        break
    
    if i%10==0: print(f"  {i}...")

io.close()
