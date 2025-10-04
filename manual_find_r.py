#!/usr/bin/env python3
from pwn import *
from math import gcd
from functools import reduce

context.log_level='warn'

io = remote('94.237.57.155', 53014, level='error')
io.timeout = 3

# Get initial prompt
io.recv()

# Get n,e,c
io.sendline(b'3')
io.recvuntil(b':\n')
n,e,c = eval(io.recvline())
print(f"[+] n={n.bit_length()}bits")

# Generate primes
primes = []
for i in range(80):
    io.recv()  # menu
    io.sendline(b'1')
    io.recvuntil(b'!\n')
    p = int(io.recvline())
    primes.append(p)
    if i%20==0: print(f"  {i} primes...")

print(f"[+] Got {len(primes)} primes")

# GCD of diffs
diffs = [abs(primes[i]-primes[i+1]) for i in range(len(primes)-1)]
r = reduce(gcd, diffs)
print(f"[+] GCD: {r.bit_length()}bits")

io.close()

if r > 1:
    open('/workspace/r_and_primes.txt','w').write(f"r_cand={r}\nn={n}\ne={e}\nc={c}\n")
    print(f"[+] Saved")
