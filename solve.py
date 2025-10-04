#!/usr/bin/env python3

from pwn import *
from math import gcd
from functools import reduce
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import unpad

# Conectar al servidor
# host, port = "94.237.57.155", 53014
# io = remote(host, port)

# Para testing local
io = process(["python3", "/workspace/crypto_raining_primes/server.py"])

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

# Paso 1: Generar varios primos para encontrar r
print("[+] Generando primos para encontrar r...")
primes = []
for i in range(10):
    p = generate_prime()
    primes.append(p)
    print(f"    Primo {i+1}: {p}")

# Paso 2: Usar GCD para encontrar r
print("\n[+] Calculando r usando GCD de diferencias de primos...")
differences = [primes[i+1] - primes[i] for i in range(len(primes)-1)]
r = reduce(gcd, differences)
print(f"    r candidato: {r}")

# Verificar que r es primo y del tamaño correcto (640 bits)
from Crypto.Util.number import isPrime
if isPrime(r) and r.bit_length() == 640:
    print(f"    [✓] r es primo de 640 bits!")
else:
    print(f"    [!] r no es válido, necesitamos más primos o un enfoque diferente")
    print(f"    r.bit_length() = {r.bit_length()}, isPrime(r) = {isPrime(r)}")
    
    # Intentar con GCD de los mismos primos
    r = reduce(gcd, primes)
    print(f"    r candidato (GCD directo): {r}")
    
    if not isPrime(r):
        # Intentar factores de r
        print(f"    [!] Probando con factores de r...")
        # Podría ser un múltiplo de r

# Paso 3: Obtener la flag encriptada
print("\n[+] Obteniendo flag encriptada...")
n, e, c = get_encrypted_flag()
print(f"    n = {n}")
print(f"    e = {e}")
print(f"    c = {c}")

# Paso 4: Factorizar n
# Los primos p y q en n también son de la forma a*r + b
# Entonces p ≡ b_p (mod r) y q ≡ b_q (mod r)
# n ≡ b_p * b_q (mod r)

print(f"\n[+] Factorizando n usando r...")
print(f"    n % r = {n % r}")

# Usar los primos generados para encontrar posibles residuos
residues = [p % r for p in primes]
print(f"    Residuos posibles: {set(residues)}")

# Intentar factorizar n buscando p de la forma a*r + residuo
# donde residuo es uno de los residuos que vimos
def try_factor_n(n, r, residues, max_attempts=10000):
    """
    Intenta factorizar n sabiendo que p y q son de la forma a*r + b
    donde b es uno de los residuos conocidos
    """
    from Crypto.Util.number import isPrime, GCD
    
    # n = p * q donde p, q son de la forma a*r + b
    # Sabemos que b es pequeño (256 bits)
    # Intentemos buscar p haciendo GCD(n, prod(primes_generated))
    
    # Primero intentemos si alguno de los primos generados divide a n
    for p in primes:
        if n % p == 0:
            q = n // p
            print(f"    [✓] Encontrado! p = {p}, q = {q}")
            return p, q
    
    # Si no, intentemos usar el hecho de que p ≡ residuo (mod r)
    # y buscar sistemáticamente
    n_mod_r = n % r
    
    # Para cada residuo, intentar encontrar el otro
    for res_p in set(residues):
        # Si p ≡ res_p (mod r), entonces q ≡ n_mod_r * inv(res_p) (mod r)
        if GCD(res_p, r) == 1:
            res_q = (n_mod_r * pow(res_p, -1, r)) % r
            
            # Buscar p de la forma a*r + res_p cerca de sqrt(n)
            sqrt_n = int(n ** 0.5)
            
            # Calcular el a apropiado
            a_start = (sqrt_n - res_p) // r
            
            for a_offset in range(-1000, 1000):
                a = a_start + a_offset
                if a <= 0:
                    continue
                    
                p = a * r + res_p
                if p > 0 and n % p == 0:
                    q = n // p
                    if isPrime(p) and isPrime(q):
                        print(f"    [✓] Encontrado! p = {p}, q = {q}")
                        return p, q
    
    return None, None

p, q = try_factor_n(n, r, residues)

if p and q:
    # Paso 5: Desencriptar
    print("\n[+] Desencriptando...")
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    
    # m es el texto cifrado de AES
    enc_flag = long_to_bytes(m)
    print(f"    Flag encriptada con AES: {enc_flag.hex()}")
    
    # Necesitamos la clave AES... pero no la tenemos directamente
    print("\n[!] Necesitamos recuperar la clave AES...")
    print("[!] Este es el siguiente paso del desafío...")
else:
    print("\n[!] No se pudo factorizar n con este método")

io.close()
