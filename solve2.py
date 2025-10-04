#!/usr/bin/env python3

from pwn import *
from math import gcd
from functools import reduce
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long, isPrime, GCD
from Crypto.Util.Padding import unpad
import itertools

# Conectar al servidor
host, port = "94.237.57.155", 53014
io = remote(host, port)

# Para testing local
# io = process(["python3", "/workspace/crypto_raining_primes/server.py"])

def menu_option(option):
    io.recvuntil(b'> ')
    io.sendline(str(option).encode())

def generate_prime():
    menu_option(1)
    io.recvuntil(b"It's raining primes!\n")
    prime = int(io.recvline().strip())
    return prime

def get_encrypted_flag():
    menu_option(3)
    io.recvuntil(b'Encrypted flag:\n')
    data = eval(io.recvline().strip())
    return data

# Paso 1: Generar muchos primos para encontrar r
print("[+] Generando primos para encontrar r...")
primes = []
num_primes = 20
for i in range(num_primes):
    p = generate_prime()
    primes.append(p)
    print(f"    Primo {i+1}: {p.bit_length()} bits")

# Paso 2: Encontrar r usando GCD de pares de primos
# La idea es que si p1 = a1*r + b1 y p2 = a2*r + b2, entonces
# GCD(p1, p2) podría darnos información sobre r
# Pero mejor: GCD(p1-p2, p1-p3, ...) podría darnos múltiplos de r

print("\n[+] Intentando encontrar r con GCD de diferencias...")
differences = []
for i in range(len(primes)):
    for j in range(i+1, len(primes)):
        diff = abs(primes[i] - primes[j])
        differences.append(diff)

# Calcular GCD de todas las diferencias
r_candidate = reduce(gcd, differences)
print(f"    GCD de todas las diferencias: {r_candidate}")
print(f"    Bits: {r_candidate.bit_length()}")

# Si r_candidate no es primo o no tiene el tamaño correcto, intentar con sus factores
if not isPrime(r_candidate) or r_candidate.bit_length() != 640:
    print(f"    [!] r_candidate no es un primo de 640 bits")
    print(f"    [*] Intentando factorizar r_candidate...")
    
    # Intentar dividir por pequeños factores
    r = r_candidate
    for small_prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        while r % small_prime == 0:
            r = r // small_prime
    
    print(f"    r después de eliminar factores pequeños: {r}")
    print(f"    Bits: {r.bit_length()}, isPrime: {isPrime(r)}")
    
    # Intentar encontrar el factor de 640 bits
    # Probar con subconjuntos de diferencias
    if r.bit_length() < 640:
        print(f"    [!] Probando con diferentes subconjuntos de primos...")
        # Probar GCD de diferentes pares
        for i in range(min(10, len(primes))):
            for j in range(i+1, min(10, len(primes))):
                g = gcd(primes[i], primes[j])
                if g > 1 and isPrime(g) and g.bit_length() == 640:
                    r = g
                    print(f"    [✓] Encontrado r = {r}")
                    break
    
    r_candidate = r

r = r_candidate
print(f"\n[+] r final: {r}")
print(f"    Bits: {r.bit_length()}, isPrime: {isPrime(r)}")

# Verificar que los primos generados son consistentes con este r
print(f"\n[+] Verificando primos con r...")
residues = []
for i, p in enumerate(primes[:5]):
    residue = p % r
    residues.append(residue)
    print(f"    p{i+1} % r = {residue} ({residue.bit_length()} bits)")

# Paso 3: Obtener la flag encriptada
print("\n[+] Obteniendo flag encriptada...")
n, e, c = get_encrypted_flag()
print(f"    n = {n.bit_length()} bits")
print(f"    e = {e}")
print(f"    c = {c.bit_length()} bits")

n_mod_r = n % r
print(f"    n % r = {n_mod_r}")

# Paso 4: Intentar factorizar n
# n = p * q donde p = a1*r + b1, q = a2*r + b2
# Entonces n ≡ b1*b2 (mod r)

print(f"\n[+] Factorizando n...")

# Método 1: Ver si alguno de los primos generados divide a n
for i, p in enumerate(primes):
    if n % p == 0:
        q = n // p
        print(f"    [✓] Encontrado! p = primes[{i}], q = n // p")
        print(f"    p = {p}")
        print(f"    q = {q}")
        
        # Desencriptar
        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)
        m = pow(c, d, n)
        enc_flag = long_to_bytes(m)
        
        print(f"\n[+] Flag encriptada con AES: {enc_flag.hex()}")
        print(f"    Longitud: {len(enc_flag)} bytes")
        
        # Ahora necesitamos la clave AES...
        # Esto requiere otro ataque
        break
else:
    print(f"    [!] Ningún primo generado divide a n")
    
    # Método 2: Usar el ataque de Coppersmith o similar
    # Esto requiere sage o algoritmos más avanzados
    print(f"    [!] Se requiere un ataque más sofisticado (Coppersmith, etc.)")

io.close()
