#!/usr/bin/env python3
from pwn import *
import json

context.log_level='error'

primes = []
ns = []

for session in range(3):
    io = remote('94.237.57.155', 53014)
    io.timeout = 3
    
    # Get n
    io.sendlineafter(b'> ', b'3')
    io.recvline()
    n,e,c = eval(io.recvline())
    ns.append((n,e,c))
    
    # Get primes
    for i in range(30):
        io.sendlineafter(b'> ', b'1')
        io.recvline()
        p = int(io.recvline())
        primes.append(p)
    
    io.close()
    print(f"Session {session+1}: n={n.bit_length()}bits, {len(primes)} total primes")

# Save
data = {'primes': primes, 'ns': ns}
json.dump(data, open('/workspace/collected.json', 'w'))
print(f"Saved {len(primes)} primes and {len(ns)} ns")
