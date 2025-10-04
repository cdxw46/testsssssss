#!/usr/bin/env python3
import json
from math import gcd
from functools import reduce

data = json.load(open('/workspace/collected.json'))
primes = data['primes']
ns = data['ns']

print(f"[+] Analyzing {len(primes)} primes and {len(ns)} ns")

# Check if any prime divides any n
print("\n[+] Checking if primes divide ns...")
for i, (n,e,c) in enumerate(ns):
    for j, p in enumerate(primes):
        if n % p == 0:
            print(f"[✓] FOUND! prime[{j}] divides n[{i}]!")
            print(f"    p = {p}")
            print(f"    q = {n//p}")
            
            from Crypto.Util.number import long_to_bytes
            phi = (p-1)*((n//p)-1)
            d = pow(e,-1,phi)
            enc = long_to_bytes(pow(c,d,n))
            print(f"    AES_encrypted: {enc.hex()}")
            open('/workspace/aes_enc.bin','wb').write(enc)
            open('/workspace/factorization.txt','w').write(f"n_idx={i}\np={p}\nq={n//p}\nenc={enc.hex()}\n")
            exit(0)

print("[!] No primes divide any n")

# Check GCD between ns
print("\n[+] Checking GCD between ns...")
for i in range(len(ns)):
    for j in range(i+1, len(ns)):
        g = gcd(ns[i][0], ns[j][0])
        if g > 1 and g < ns[i][0]:
            print(f"[✓] GCD(n[{i}], n[{j}]) = {g.bit_length()}bits")
            print(f"    Factor: {g}")

# Try to find r using GCD of differences
print("\n[+] Finding r using GCD of differences...")
diffs = [abs(primes[i]-primes[i+1]) for i in range(len(primes)-1)]
r_cand = reduce(gcd, diffs)
print(f"    GCD of diffs: {r_cand.bit_length()}bits")

# Remove small factors
r = r_cand
for f in [2,3,5,7,11,13,17,19,23,29,31]:
    while r%f==0: r//=f

print(f"    After removing small factors: {r.bit_length()}bits")

from Crypto.Util.number import isPrime
if isPrime(r) and r.bit_length()==640:
    print(f"[✓] Found r!")
    open('/workspace/r_value.txt','w').write(str(r))
else:
    print(f"[!] r candidate is not a 640-bit prime")
    print(f"    isPrime: {isPrime(r)}, bits: {r.bit_length()}")
