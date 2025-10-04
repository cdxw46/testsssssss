#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import long_to_bytes, GCD, isPrime
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
import sys

# Conectar al servidor con timeout
host, port = "94.237.57.155", 53014

context.log_level = 'info'

try:
    io = remote(host, port, timeout=10)
except Exception as e:
    print(f"[!] Error conectando: {e}")
    sys.exit(1)

def menu_option(option, timeout=5):
    try:
        io.recvuntil(b'> ', timeout=timeout)
        io.sendline(str(option).encode())
    except Exception as e:
        print(f"[!] Error en menu_option: {e}")
        raise

def generate_prime(timeout=10):
    try:
        menu_option(1, timeout=timeout)
        io.recvuntil(b"It's raining primes!\n", timeout=timeout)
        prime = int(io.recvline(timeout=timeout).strip())
        return prime
    except Exception as e:
        print(f"[!] Error en generate_prime: {e}")
        raise

def get_encrypted_flag(timeout=10):
    try:
        menu_option(3, timeout=timeout)
        io.recvuntil(b'Encrypted flag:\n', timeout=timeout)
        data = eval(io.recvline(timeout=timeout).strip())
        return data
    except Exception as e:
        print(f"[!] Error en get_encrypted_flag: {e}")
        raise

# Estrategia: La clave está en entender que podemos manipular la clave AES
# a través de update_key. Primero necesitamos obtener n, e, c

print("[+] Paso 1: Obtener flag encriptada...")
try:
    n, e, c = get_encrypted_flag(timeout=10)
    print(f"    n = {n.bit_length()} bits")
    print(f"    e = {e}")
    print(f"    c = {c.bit_length()} bits")
except Exception as e:
    print(f"[!] Error obteniendo flag: {e}")
    io.close()
    sys.exit(1)

print("\n[+] Paso 2: Generar primos para encontrar factores...")
primes = []
max_primes = 200

try:
    for i in range(max_primes):
        try:
            p = generate_prime(timeout=10)
            primes.append(p)
            
            # Verificar si divide a n
            if n % p == 0:
                q = n // p
                print(f"\n[✓] ¡FACTOR ENCONTRADO! (primo #{i+1})")
                print(f"    p = {p}")
                print(f"    q = {q}")
                
                # Desencriptar RSA
                phi = (p - 1) * (q - 1)
                d = pow(e, -1, phi)
                m = pow(c, d, n)
                enc_flag_bytes = long_to_bytes(m)
                
                print(f"\n[+] Flag encriptada con AES (hex):")
                print(f"    {enc_flag_bytes.hex()}")
                
                # Guardar para siguiente paso
                with open('/workspace/rsa_decrypted.txt', 'w') as f:
                    f.write(f"p = {p}\n")
                    f.write(f"q = {q}\n")
                    f.write(f"enc_flag_hex = {enc_flag_bytes.hex()}\n")
                
                # Ahora necesitamos la clave AES
                # Podemos usar update_key para manipularla
                print(f"\n[+] Paso 3: Recuperar clave AES...")
                print(f"    La clave AES está protegida por un esquema HNP-like")
                print(f"    Necesitamos usar update_key para extraer bits de la clave")
                
                io.close()
                exit(0)
            
            if (i + 1) % 10 == 0:
                print(f"    Generados {i+1} primos...")
                
        except KeyboardInterrupt:
            print(f"\n[!] Interrumpido por usuario")
            break
        except Exception as e:
            print(f"[!] Error generando primo {i+1}: {e}")
            break
            
except Exception as e:
    print(f"[!] Error en bucle principal: {e}")

print(f"\n[!] No se encontró factor en {len(primes)} primos")
io.close()
