#!/usr/bin/env python3
from pwn import *
from math import gcd
from functools import reduce

context.log_level='error'

io = remote('94.237.57.155', 53014)
io.timeout = 3

# Get n,e,c
io.sendlineafter(b'> ', b'3')
io.recvline()
n,e,c = eval(io.recvline())

print(f"[+] n={n.bit_length()}bits, e={e}")

# Generate many primes from SAME session
print(f"[+] Generating primes from same session...")
primes = []
for i in range(100):
    io.sendlineafter(b'> ', b'1')
    io.recvline()
    p = int(io.recvline())
    primes.append(p)
    if i%20==0: print(f"  {i}...")

print(f"[+] Got {len(primes)} primes")

# Calculate r using GCD of differences
print(f"[+] Calculating r...")
diffs = [abs(primes[i]-primes[i+1]) for i in range(len(primes)-1)]
r_cand = reduce(gcd, diffs)

print(f"    GCD of diffs: {r_cand.bit_length()}bits")

# Try to clean r
r = r_cand
for f in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]:
    while r%f==0: 
        r//=f
        print(f"      Divided by {f}")

print(f"    After cleaning: {r.bit_length()}bits")

from Crypto.Util.number import isPrime
print(f"    isPrime(r): {isPrime(r)}")

if r > 2**630 and r < 2**650:
    print(f"[+] Saving r...")
    open('/workspace/r_value.txt','w').write(str(r))
    open('/workspace/session_data.txt','w').write(f"n={n}\ne={e}\nc={c}\nr={r}\n")

io.close()
