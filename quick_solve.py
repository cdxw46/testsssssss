#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

context.log_level = 'error'

host, port = "94.237.57.155", 53014

print("[+] Conectando...")
io = remote(host, port, timeout=5)

# Obtener n, e, c
io.recvuntil(b'> ', timeout=3)
io.sendline(b'3')
io.recvuntil(b'Encrypted flag:\n', timeout=3)
n, e, c = eval(io.recvline(timeout=3).strip())

print(f"[+] n = {n.bit_length()} bits")
print(f"[+] Generando primos...")

# Generar primos rápidamente
primes = []
for i in range(150):
    try:
        io.recvuntil(b'> ', timeout=3)
        io.sendline(b'1')
        io.recvuntil(b"It's raining primes!\n", timeout=3)
        p = int(io.recvline(timeout=3).strip())
        primes.append(p)
        
        # Verificar si divide n
        if n % p == 0:
            q = n // p
            print(f"\n[✓] Factor encontrado! (primo #{i+1})")
            
            # Desencriptar RSA
            phi = (p - 1) * (q - 1)
            d = pow(e, -1, phi)
            m = pow(c, d, n)
            enc_flag = long_to_bytes(m)
            
            print(f"[+] Flag encriptada (AES): {enc_flag.hex()}")
            
            # Ahora usar update_key para extraer la clave
            # k0_i = a_i * r + (2*b_i + key_bit_i)
            # Si enviamos k1 = [r+1, r+1, ...], entonces:
            # k_i = k0_i * (r+1) = k0_i*r + k0_i
            # (k_i % r) % 2 = k0_i % 2 = (2*b_i + key_bit_i) % 2
            
            # Necesitamos 256 bits (32 bytes) para la clave
            # Enviar k1 con 256 elementos
            
            print(f"[+] Extrayendo clave AES...")
            
            # Primero generar un primo para estimar r
            io.recvuntil(b'> ', timeout=3)
            io.sendline(b'1')
            io.recvuntil(b"It's raining primes!\n", timeout=3)
            prime_sample = int(io.recvline(timeout=3).strip())
            
            # r es aproximadamente el GCD de primos, probemos valores
            # Sabemos que r es de 640 bits, pero no lo conocemos exactamente
            # Vamos a intentar adivinar la clave por fuerza bruta (poco probable)
            
            # O mejor: la clave inicial era aleatoria de 256 bits
            # No podemos recuperarla fácilmente sin r
            
            print(f"[!] Se necesita r para continuar")
            print(f"[!] Intentando encontrar r con los primos generados...")
            
            from math import gcd
            from functools import reduce
            
            # GCD de diferencias
            if len(primes) >= 2:
                diffs = [abs(primes[i] - primes[i+1]) for i in range(len(primes)-1)]
                r_candidate = reduce(gcd, diffs)
                print(f"    GCD de diferencias: {r_candidate.bit_length()} bits")
                
                # Remover factores pequeños
                r = r_candidate
                for factor in [2, 3, 5, 7, 11, 13]:
                    while r % factor == 0:
                        r = r // factor
                        
                print(f"    r candidate: {r.bit_length()} bits")
                
                if r > 2**630:
                    print(f"    [*] Usando r = {r}")
                    
                    # Ahora podemos extraer la clave
                    # Enviar k1 con valores > r y < 2^384 * r
                    k1 = [r + 1] * 256
                    
                    io.recvuntil(b'> ', timeout=3)
                    io.sendline(b'2')
                    io.recvuntil(b'Encrypted key:\n', timeout=3)
                    io.sendline(str(k1).encode())
                    
                    # La clave ha sido actualizada, ahora obtener la nueva flag
                    io.recvuntil(b'> ', timeout=3)
                    io.sendline(b'3')
                    io.recvuntil(b'Encrypted flag:\n', timeout=3)
                    n2, e2, c2 = eval(io.recvline(timeout=3).strip())
                    
                    # Desencriptar con la nueva configuración
                    d2 = pow(e2, -1, phi)
                    m2 = pow(c2, d2, n2)
                    enc_flag2 = long_to_bytes(m2)
                    
                    print(f"[+] Nueva flag encriptada: {enc_flag2.hex()}")
            
            io.close()
            exit(0)
            
        if (i+1) % 25 == 0:
            print(f"    {i+1} primos...")
            
    except Exception as e:
        print(f"[!] Error: {e}")
        break

print(f"[!] No encontrado en {len(primes)} primos")
io.close()
