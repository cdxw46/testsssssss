#!/usr/bin/env python3
import json
from fpylll import IntegerMatrix, LLL
from Crypto.Util.number import isPrime

# Load collected primes
data = json.load(open('/workspace/collected.json'))
primes = data['primes'][:30]  # Use first 30 primes from same session

print(f"[+] Using {len(primes)} primes for lattice attack")

# Build lattice matrix
# The idea: if p_i = a_i * r + b_i, we want to find r
# We build a matrix where rows represent primes and try to find
# a short vector that represents r

n = len(primes)
M = IntegerMatrix(n+1, n+1)

# Scale factor
scale = 2**300

# Fill matrix
# Each row i (except last): [p_i, 1, 0, 0, ..., 0]
# This represents: coefficient * p_i + offset
for i in range(n):
    M[i, i] = scale
    M[i, n] = primes[i]

# Last row for balance
for j in range(n):
    M[n, j] = 0
M[n, n] = 1

print("[+] Running LLL reduction...")
M_red = LLL.reduction(M)

print("[+] Checking reduced basis vectors...")
for i in range(min(10, n+1)):
    # Get the vector
    vec = [M_red[i, j] for j in range(n+1)]
    
    # The last component might be related to r
    candidate = abs(vec[n])
    
    if 2**630 < candidate < 2**650:
        print(f"  Row {i}: candidate = {candidate.bit_length()} bits")
        if isPrime(candidate):
            print(f"    [✓] Is prime!")
            open('/workspace/r_lattice.txt','w').write(str(candidate))
            print(f"    Saved to r_lattice.txt")
            break

print("[+] Done")
