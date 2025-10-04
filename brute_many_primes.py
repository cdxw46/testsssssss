#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import long_to_bytes

context.log_level='error'

io = remote('94.237.57.155', 53014)
io.timeout = 3

# Get n,e,c
io.recv()
io.sendline(b'3')
io.recvuntil(b':\n')
n,e,c = eval(io.recvline())

print(f"[+] Trying up to 1000 primes...")

for i in range(1000):
    try:
        io.recv()
        io.sendline(b'1')
        io.recvuntil(b'!\n')
        p = int(io.recvline())
        
        if n % p == 0:
            print(f"\n[✓] FOUND at {i}!")
            q = n//p
            phi = (p-1)*(q-1)
            d = pow(e,-1,phi)
            enc = long_to_bytes(pow(c,d,n))
            print(f"AES: {enc.hex()}")
            open('/workspace/success.txt','w').write(f"i={i}\nenc={enc.hex()}\nn={n}\ne={e}\nc={c}\np={p}\nq={q}\n")
            io.close()
            exit(0)
        
        if i%50==0 and i>0: print(f"  {i}...")
    except Exception as e:
        print(f"Error at {i}: {e}")
        break

print(f"[!] Not found")
io.close()
