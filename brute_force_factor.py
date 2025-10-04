#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import long_to_bytes, GCD
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

# Conectar al servidor
host, port = "94.237.57.155", 53014
io = remote(host, port)

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

# Obtener la flag encriptada primero
print("[+] Obteniendo flag encriptada...")
n, e, c = get_encrypted_flag()
print(f"    n = {n.bit_length()} bits")
print(f"    e = {e}")

# Ahora generar primos y ver si alguno divide a n
print("\n[+] Generando primos y buscando factores de n...")
primes = []
for i in range(1000):  # Generar muchos primos
    p = generate_prime()
    primes.append(p)
    
    # Verificar si este primo divide a n
    if n % p == 0:
        q = n // p
        print(f"\n[✓] ¡ENCONTRADO! Primo {i+1} divide a n!")
        print(f"    p = {p}")
        print(f"    q = {q}")
        
        # Desencriptar RSA
        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)
        m = pow(c, d, n)
        enc_flag_bytes = long_to_bytes(m)
        
        print(f"\n[+] Flag encriptada con AES:")
        print(f"    {enc_flag_bytes.hex()}")
        print(f"    Longitud: {len(enc_flag_bytes)} bytes")
        
        # Ahora necesitamos la clave AES
        # Esto es otro desafío...
        print(f"\n[!] Necesitamos recuperar la clave AES de 32 bytes")
        print(f"[!] Esto requiere explotar la función update_key")
        
        # Guardar información para el siguiente paso
        with open('/workspace/factorization.txt', 'w') as f:
            f.write(f"p = {p}\n")
            f.write(f"q = {q}\n")
            f.write(f"n = {n}\n")
            f.write(f"e = {e}\n")
            f.write(f"c = {c}\n")
            f.write(f"enc_flag_hex = {enc_flag_bytes.hex()}\n")
        
        print(f"\n[+] Información guardada en factorization.txt")
        io.close()
        exit(0)
    
    if (i + 1) % 50 == 0:
        print(f"    Generados {i+1} primos...")
        
        # También verificar GCD por si acaso
        g = GCD(n, primes[-1])
        if g > 1 and g < n:
            print(f"      [!] GCD encontrado: {g}")

print("\n[!] No se encontró ningún factor después de generar muchos primos")
io.close()
