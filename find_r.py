#!/usr/bin/env python3

from pwn import *
from fpylll import IntegerMatrix, LLL
import itertools

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

# Generar varios primos
print("[+] Generando primos...")
primes = []
for i in range(15):
    p = generate_prime()
    primes.append(p)
    print(f"    Primo {i+1}: {p}")

print("\n[+] Usando LLL para encontrar r...")

# Método de lattice:
# Si p_i = a_i * r + b_i donde b_i es pequeño,
# podemos construir un lattice y usar LLL para encontrar r

# Construir matriz de lattice
# Cada fila será [p_i, 1, 0, 0, ...]
# Queremos encontrar una combinación lineal que dé r

n = len(primes)
# Crear matriz con n+1 filas y n+1 columnas
# La idea es que [c_1, c_2, ..., c_n] * primes - r * [c_1*a_1, c_2*a_2, ..., c_n*a_n] = small

# Método alternativo: usar diferencias de primos
# p_i - p_j = (a_i - a_j) * r + (b_i - b_j)
# Si tenemos suficientes diferencias, podemos encontrar r

differences = []
for i in range(len(primes)):
    for j in range(i+1, len(primes)):
        diff = abs(primes[i] - primes[j])
        differences.append(diff)

print(f"    Generadas {len(differences)} diferencias")

# Usar lattice para encontrar r
# Construir una matriz donde cada fila es una diferencia
# y queremos encontrar una combinación que sea r

# Tamaño del lattice - usamos las primeras diferencias
num_diffs = min(20, len(differences))
M = IntegerMatrix(num_diffs + 1, num_diffs + 1)

# Escala para ayudar al LLL
scale = 2**640  # Aproximadamente el tamaño de r

# Llenar la matriz
for i in range(num_diffs):
    M[i, i] = differences[i]
    M[i, num_diffs] = scale

# Última fila para el balance
for j in range(num_diffs):
    M[num_diffs, j] = 0
M[num_diffs, num_diffs] = scale * scale

print("    Ejecutando LLL...")
M_lll = LLL.reduction(M)

print("    Primeras filas reducidas:")
for i in range(min(5, num_diffs + 1)):
    row = [M_lll[i, j] for j in range(num_diffs + 1)]
    # Calcular la norma
    norm = sum(abs(x) for x in row)
    print(f"      Fila {i}: norma = {norm}")
    
    # Ver si algún elemento es un candidato para r
    for val in row:
        val = abs(val)
        if val > 2**600 and val < 2**680:
            print(f"        Candidato: {val} ({val.bit_length()} bits)")
            
            # Verificar si es primo
            from Crypto.Util.number import isPrime
            if isPrime(val):
                print(f"        [✓] ¡Es primo!")
                r = val
                
                # Verificar con los primos
                print(f"\n[+] Verificando r = {r}")
                residues = [p % r for p in primes[:5]]
                print(f"    Residuos: {[res.bit_length() for res in residues]}")
                
                if all(res.bit_length() <= 260 for res in residues):
                    print(f"    [✓] ¡Todos los residuos son pequeños!")
                    io.close()
                    
                    # Guardar r para usarlo después
                    with open('/workspace/r_value.txt', 'w') as f:
                        f.write(str(r))
                    
                    print(f"\n[+] r guardado en r_value.txt")
                    exit(0)

print("\n[!] No se encontró r con este método")

# Método alternativo: búsqueda por fuerza bruta inteligente
# Sabemos que todos los primos son p = a * r + b donde b < 2^256
# Entonces p % r = b < 2^256

print("\n[+] Intentando método alternativo...")
print("    Buscando r tal que todos los primos tengan residuos pequeños...")

# Tomar dos primos y buscar divisores comunes de forma más inteligente
# Si p1 = a1*r + b1 y p2 = a2*r + b2, entonces gcd(p1-b1, p2-b2) contiene r
# Pero no conocemos b1 y b2...

# Otra idea: si r es de 640 bits y conocemos que está en los primos,
# podemos buscar factores grandes comunes

from math import gcd as math_gcd

print("    Probando GCDs de primos cercanos...")
for b1 in range(0, 2**20, 2**10):  # Probar algunos valores pequeños de b
    for i in range(min(3, len(primes))):
        p_adjusted = primes[i] - b1
        for j in range(i+1, min(5, len(primes))):
            for b2 in range(0, 2**20, 2**10):
                q_adjusted = primes[j] - b2
                g = math_gcd(p_adjusted, q_adjusted)
                if g > 2**630 and g < 2**650:
                    print(f"      Candidato: {g.bit_length()} bits")
                    from Crypto.Util.number import isPrime
                    if isPrime(g):
                        print(f"      [✓] ¡Es primo! r = {g}")
                        r = g
                        with open('/workspace/r_value.txt', 'w') as f:
                            f.write(str(r))
                        io.close()
                        exit(0)

io.close()
print("\n[!] No se pudo encontrar r")
