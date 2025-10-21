#!/usr/bin/env python3
from Crypto.Cipher import Salsa20

# Los datos en rodata son strings ASCII que representan hexadecimal
# 0x39ca0: "ef39f4f20e76e33b" 
# 0x39cb0: "d25f4db338e81b10"

# Estos forman una clave de 32 bytes cuando se interpretan como una cadena hex de 64 caracteres
key_hex = 'ef39f4f20e76e33bd25f4db338e81b10'
print(f"Key hex string: {key_hex}")

# Espera, eso solo da 16 bytes. Necesito 32 bytes para Salsa20.
# Mirando el código, se cargan 32 bytes desde 0x39ca0
# Déjame revisar si la clave es de 16 bytes duplicada o algo así

# Primero intentemos con Salsa20/12 que usa claves de 16 bytes
# O tal vez la clave se repite

# Intentemos varias opciones
print("\n=== Opción 1: Clave de 16 bytes duplicada ===")
key_16 = bytes.fromhex(key_hex)
key_32_dup = key_16 + key_16
print(f"Key duplicada (32 bytes): {key_32_dup.hex()}")

# El nonce necesita 8 bytes
nonce_hex = '3a072c4d'
# Tal vez necesito padding
nonce_8 = bytes.fromhex(nonce_hex) + b'\x00\x00\x00\x00'
print(f"Nonce con padding (8 bytes): {nonce_8.hex()}")

# Los bytes esperados
expected = bytes.fromhex('05055fb1a329a8d558d9f556a6cb31f324432a31c99dec72e33eb66f62ad1bf9')

try:
    cipher = Salsa20.new(key=key_32_dup, nonce=nonce_8)
    password = cipher.decrypt(expected)
    print(f"\nPassword: {password}")
    if all(32 <= b < 127 for b in password[:20] if b != 0):
        print(f"¡Parece ASCII!: {password.decode('ascii', errors='ignore')}")
except Exception as e:
    print(f"Error: {e}")

# Opción 2: Tal vez el nonce es "d4c270a3" (8 caracteres)
print("\n=== Opción 2: Nonce completo de movabs ===")
# El movabs carga 0x3361303732633464 que es "d4c270a3" al revés
nonce_full = b'd4c270a3'
print(f"Nonce completo: {nonce_full} ({nonce_full.hex()})")

try:
    cipher2 = Salsa20.new(key=key_32_dup, nonce=nonce_full)
    password2 = cipher2.decrypt(expected)
    print(f"\nPassword: {password2}")
    password_clean = password2.rstrip(b'\x00').rstrip(b'\n')
    if all(32 <= b < 127 for b in password_clean if b != 0):
        print(f"¡ES ASCII!: {password_clean.decode('ascii')}")
except Exception as e:
    print(f"Error: {e}")

# Opción 3: Interpretar los datos de forma diferente
print("\n=== Opción 3: Datos directos de rodata ===")
# En rodata tenemos:
# 39ca0: 65663339663466323065373665333362  (que decodifica a "ef39f4f20e76e33b")
# 39cb0: 64323566346462333338653831623130  (que decodifica a "d25f4db338e81b10")

# Pero tal vez debo usar los bytes directos, no decodificarlos
key_direct = bytes.fromhex('6566333966346632306537366533336264323566346462333338653831623130')
print(f"Key directa: {key_direct} (len={len(key_direct)})")
print(f"Key directa ASCII: {key_direct.decode('ascii')}")

# Esta es la cadena hexadecimal completa
key_final = bytes.fromhex(key_direct.decode('ascii'))
print(f"Key final: {key_final.hex()} (len={len(key_final)})")