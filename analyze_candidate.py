#!/usr/bin/env python3

from Crypto.Util.number import isPrime, GCD
from sympy import factorint, primefactors
import math

# El candidato que encontramos con LLL
candidate = 4562440617622195218641171605700291324893228507248559930579192517899275167208677386505912811317371399778642309573594407310688704721375437998252661319722214188251994674360264950082874192246603776

print(f"[+] Analizando candidato de LLL:")
print(f"    Valor: {candidate}")
print(f"    Bits: {candidate.bit_length()}")
print(f"    Es primo: {isPrime(candidate)}")

# Intentar factorizar
print(f"\n[+] Intentando factorizar...")
print(f"    Buscando factores pequeños...")

r_candidate = candidate
small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

factors_found = []
for p in small_primes:
    count = 0
    while r_candidate % p == 0:
        r_candidate = r_candidate // p
        count += 1
    if count > 0:
        factors_found.append((p, count))
        print(f"      Factor {p}^{count}")

print(f"\n    Después de eliminar factores pequeños:")
print(f"      Valor: {r_candidate}")
print(f"      Bits: {r_candidate.bit_length()}")
print(f"      Es primo: {isPrime(r_candidate)}")

if r_candidate.bit_length() == 640 and isPrime(r_candidate):
    print(f"\n[✓] ¡Encontrado! r = {r_candidate}")
    
    # Guardar r
    with open('/workspace/r_value.txt', 'w') as f:
        f.write(str(r_candidate))
    print(f"[+] r guardado en r_value.txt")
else:
    print(f"\n[!] El candidato después de eliminar factores no es un primo de 640 bits")
    
    # Tal vez es 2*r o algo así
    if r_candidate.bit_length() == 641:
        r2 = r_candidate // 2
        print(f"\n[+] Probando r = candidate // 2:")
        print(f"    Bits: {r2.bit_length()}")
        print(f"    Es primo: {isPrime(r2)}")
        
        if isPrime(r2) and r2.bit_length() == 640:
            print(f"\n[✓] ¡Encontrado! r = {r2}")
            with open('/workspace/r_value.txt', 'w') as f:
                f.write(str(r2))
            print(f"[+] r guardado en r_value.txt")
