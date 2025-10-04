#!/usr/bin/env python3
from pwn import *
from math import gcd

context.log_level='error'

io = remote('94.237.57.155', 53014)
io.timeout = 3

# Get n
io.recv()
io.sendline(b'3')
io.recvuntil(b':\n')
n,e,c = eval(io.recvline())

print(f"[+] n={n.bit_length()}bits")

# Get primes
primes = []
for i in range(50):
    io.recv()
    io.sendline(b'1')
    io.recvuntil(b'!\n')
    p = int(io.recvline())
    primes.append(p)
    
    # Try GCD with n
    g = gcd(p, n)
    if g > 1 and g < n:
        print(f"\n[✓] GCD(prime[{i}], n) = {g.bit_length()}bits!")
        if n % g == 0:
            from Crypto.Util.number import long_to_bytes
            q = n//g
            phi = (g-1)*(q-1)
            d = pow(e,-1,phi)
            enc = long_to_bytes(pow(c,d,n))
            print(f"[+] AES: {enc.hex()}")
            open('/workspace/flag_aes.bin','wb').write(enc)
            io.close()
            exit(0)
    
    if i%10==0: print(f"  {i}...")

print(f"[!] No GCD found")

# Try GCD between primes
print(f"[+] Trying GCD between primes...")
for i in range(len(primes)):
    for j in range(i+1, min(i+5, len(primes))):
        g = gcd(primes[i], primes[j])
        if g > 2**630:
            print(f"[✓] GCD(p[{i}], p[{j}]) = {g.bit_length()}bits")
            open('/workspace/r_found.txt','w').write(str(g))

io.close()
