#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import long_to_bytes

context.log_level='error'

io = remote('94.237.57.155', 53014)
io.timeout = 3

# Get n,e,c
io.sendlineafter(b'> ', b'3')
io.recvline()
n,e,c = eval(io.recvline())

print(f"[+] n={n.bit_length()}bits")
print(f"[+] Generating many primes from same session...")

# Try MANY primes from same session
for i in range(500):
    try:
        io.sendlineafter(b'> ', b'1', timeout=3)
        io.recvline(timeout=3)
        p = int(io.recvline(timeout=3))
        
        if n % p == 0:
            print(f"\n[✓] FOUND at i={i}!")
            q = n//p
            phi = (p-1)*(q-1)
            d = pow(e,-1,phi)
            enc = long_to_bytes(pow(c,d,n))
            print(f"[+] AES_enc: {enc.hex()}")
            open('/workspace/aes_enc.bin','wb').write(enc)
            open('/workspace/found.txt','w').write(f"i={i}\np={p}\nq={q}\n")
            io.close()
            exit(0)
        
        if i%25==0: print(f"  {i}...")
    except:
        break

print(f"\n[!] Not found in {i} primes")
io.close()
