#!/usr/bin/env python3
# Based on Approximate GCD problem solution
from pwn import *
from fpylll import IntegerMatrix, LLL, GSO
from Crypto.Util.number import isPrime
import json

context.log_level='error'

# Collect fresh primes from ONE session
io = remote('94.237.57.155', 53014)
io.timeout = 3

io.recv()
io.sendline(b'3')
io.recvuntil(b':\n')
n,e,c = eval(io.recvline())

print(f"[+] Collecting 40 primes from single session...")
primes = []
for i in range(40):
    io.recv()
    io.sendline(b'1')
    io.recvuntil(b'!\n')
    p = int(io.recvline())
    primes.append(p)

io.close()
print(f"[+] Got {len(primes)} primes")

# Approximate GCD lattice attack
# Build matrix where we want to find GCD(p1-x0, p2-x0, ..., pn-x0) = r
# Use x0 = p0 as reference

x0 = primes[0]
diffs = [p - x0 for p in primes[1:]]

print(f"[+] Building lattice...")
n_primes = len(diffs)
M = IntegerMatrix(n_primes+1, n_primes+1)

# Scaling
B = 2**256  # Approximate size of noise (b values)

# Matrix structure for approximate GCD
# [B   diff1  0  0  ...]
# [0   diff2  B  0  ...]
# [0   diff3  0  B  ...]
# ...

for i in range(n_primes):
    M[i, 0] = diffs[i]
    M[i, i+1] = B

# Last row
M[n_primes, 0] = x0
for j in range(1, n_primes+1):
    M[n_primes, j] = 0

print(f"[+] Running LLL...")
M_red = LLL.reduction(M)

print(f"[+] Checking results...")
for i in range(min(5, n_primes+1)):
    vec = [M_red[i, j] for j in range(n_primes+1)]
    
    # Check first component
    cand = abs(vec[0])
    if 2**630 < cand < 2**650 and isPrime(cand):
        print(f"[✓] Found r at row {i}: {cand.bit_length()} bits")
        open('/workspace/r_final.txt','w').write(f"r={cand}\nn={n}\ne={e}\nc={c}\n")
        exit(0)

print(f"[!] r not found in lattice")
