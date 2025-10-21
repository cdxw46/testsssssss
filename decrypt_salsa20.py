#!/usr/bin/env python3
from Crypto.Cipher import Salsa20

# Configuración de Salsa20 extraída del binario
# La clave parece estar en dos partes en la sección .rodata
key_hex1 = '65663339663466323065373665333362'  # en 0x39ca0
key_hex2 = '64323566346462333338653831623130'  # en 0x39cb0
nonce_hex = '3361303732633464'  # del movabs

# Convertir hex a bytes (los valores están en little-endian en memoria)
key_part1 = bytes.fromhex(key_hex1)[::-1]
key_part2 = bytes.fromhex(key_hex2)[::-1]
key = key_part1 + key_part2  # Clave de 32 bytes para Salsa20/20

nonce = bytes.fromhex(nonce_hex)[::-1]

# Los bytes esperados después del cifrado (lo que el programa compara)
expected_encrypted = bytes.fromhex('05055fb1a329a8d558d9f556a6cb31f324432a31c99dec72e33eb66f62ad1bf9')

print(f"Key (hex): {key.hex()}")
print(f"Key (ASCII): {key}")
print(f"Nonce: {nonce.hex()} ({nonce})")
print(f"Expected encrypted: {expected_encrypted.hex()}")

# Salsa20 es un cifrado de stream, así que cifrar es lo mismo que descifrar
cipher = Salsa20.new(key=key, nonce=nonce)
decrypted = cipher.decrypt(expected_encrypted)

print(f"\nDecrypted password: {decrypted}")
print(f"Decrypted (hex): {decrypted.hex()}")

# Eliminar posible newline al final
password = decrypted.rstrip(b'\n').rstrip(b'\x00')
print(f"\nPassword without newline: {password}")
print(f"Password length: {len(password)}")