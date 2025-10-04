#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

context.log_level='error'

io = remote('94.237.57.155', 53014)
io.timeout = 3

# Get n,e,c
io.recv()
io.sendline(b'3')
io.recvuntil(b':\n')
n,e,c = eval(io.recvline())

print(f"[+] n={n.bit_length()}bits")

# Generate primes to estimate r
print(f"[+] Generating primes to estimate r...")
primes = []
for i in range(20):
    io.recv()
    io.sendline(b'1')
    io.recvuntil(b'!\n')
    p = int(io.recvline())
    primes.append(p)

# Estimate r: take smallest difference divided by estimated a range
# If p1 = a1*r + b1 and p2 = a2*r + b2
# Then |p1-p2| ≈ |a1-a2|*r (ignoring b)
# If |a1-a2| = 1 (consecutive a's), then diff ≈ r

diffs = [abs(primes[i]-primes[i+1]) for i in range(len(primes)-1)]
min_diff = min(diffs)
print(f"[+] Min diff: {min_diff.bit_length()} bits")

# r is approximately min_diff (could be off by small b values)
# Let's try r_est = min_diff rounded down to nearest 2^640 range
r_est = min_diff
print(f"[+] Estimated r: {r_est.bit_length()} bits")

# Now use update_key to set all bits to 0
# Send k1 where each k1_i ≈ r_est
# But k1_i must be > r_est and <= 2^384 * r_est

# Try setting k1_i = r_est + 1 (minimum allowed value > r)
k1 = [r_est + 1] * 256

print(f"[+] Sending update_key with k1 = [r_est+1] * 256...")
io.recv()
io.sendline(b'2')
io.recvuntil(b':\n')
io.sendline(str(k1).encode())

# Get new encrypted flag
print(f"[+] Getting new encrypted flag...")
io.recv()
io.sendline(b'3')
io.recvuntil(b':\n')
n2,e2,c2 = eval(io.recvline())

print(f"[+] Got new c")

# If our attack worked, the key is now all zeros (or predictable)
# Try decrypting with all-zero key
key_zero = b'\x00' * 32

# But we still need to factor n to decrypt RSA part...
# This approach won't work without factoring n first

print(f"[!] Still need to factor n to proceed")

io.close()

# Save data
open('/workspace/attack_data.txt','w').write(f"n={n}\ne={e}\nc={c}\nc2={c2}\nr_est={r_est}\n")
