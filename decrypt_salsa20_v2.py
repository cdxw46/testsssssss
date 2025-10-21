#!/usr/bin/env python3
from Crypto.Cipher import Salsa20
import struct

# Los datos están en memoria x86-64, voy a leerlos como aparecen en el binario
# En 0x39ca0: ef39f4f20e76e33b d25f4db338e81b10
# En 0x39cb0: (ya usado arriba)

# Primero, veamos los datos tal como aparecen en rodata
key_data = bytes.fromhex('ef39f4f20e76e33bd25f4db338e81b10')  # 16 bytes desde 0x39ca0
key_data2 = bytes.fromhex('65663339663466323065373665333362')  # Continuación? O esto es ASCII

# El nonce del movabs
nonce_data = bytes.fromhex('3361303732633464')  # Esto es "d4c270a3" en ASCII al revés

# Intentemos varias combinaciones
print("=== Intento 1: Key como aparece en memoria ===")
key1 = bytes.fromhex('ef39f4f20e76e33bd25f4db338e81b1065663339663466323065373665333362')
print(f"Key1 (32 bytes): {key1.hex()}")

# Los bytes esperados
expected = bytes.fromhex('05055fb1a329a8d558d9f556a6cb31f324432a31c99dec72e33eb66f62ad1bf9')

# Salsa20 necesita clave de 32 bytes y nonce de 8 bytes
nonce = nonce_data[:8]
print(f"Nonce: {nonce.hex()} (ASCII: {nonce})")

try:
    cipher = Salsa20.new(key=key1[:32], nonce=nonce)
    decrypted = cipher.decrypt(expected)
    print(f"Decrypted: {decrypted}")
    if all(32 <= b < 127 for b in decrypted[:20]):  # Check if printable
        print(f"Looks like ASCII!")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Intento 2: Key en orden inverso ===")
# A veces los valores se almacenan en little-endian
key2_p1 = bytes.fromhex('ef39f4f20e76e33bd25f4db338e81b10')
key2_p2 = bytes.fromhex('65663339663466323065373665333362')

# Intentar como texto ASCII para la segunda parte
key2_p2_ascii = key2_p2.decode('ascii')
print(f"Segunda parte como ASCII: {key2_p2_ascii}")

# La segunda parte parece ser hexadecimal de ASCII, decodifiquémosla
key2_p2_decoded = bytes.fromhex(key2_p2_ascii)
print(f"Segunda parte decodificada: {key2_p2_decoded}")

key2 = key2_p1 + key2_p2_decoded
print(f"Key2 combinada: {key2.hex()} (len={len(key2)})")

if len(key2) == 32:
    cipher2 = Salsa20.new(key=key2, nonce=nonce)
    decrypted2 = cipher2.decrypt(expected)
    print(f"Decrypted2: {decrypted2}")
    if all(32 <= b < 127 for b in decrypted2 if b != 0):
        print(f"Looks like ASCII: {decrypted2.decode('ascii', errors='ignore')}")