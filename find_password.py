#!/usr/bin/env python3
from Crypto.Cipher import Salsa20
import sys

# Basándome en el análisis del binario:
# - El programa lee una contraseña del usuario
# - La cifra con Salsa20
# - Compara el resultado con 32 bytes esperados

# Los 32 bytes esperados (desde 0x39cc0)
expected = bytes.fromhex('05055fb1a329a8d558d9f556a6cb31f324432a31c99dec72e33eb66f62ad1bf9')

# Ahora, necesito encontrar la configuración correcta de Salsa20
# Mirando el código, veo que se cargan datos desde:
# - 0x39ca0 -> 0x90(%rsp): primer parte de la clave
# - 0x39cb0 -> 0xa0(%rsp): segunda parte de la clave  
# - movabs -> 0xc0(%rsp): nonce

# En rodata:
# 39ca0: ASCII "ef39f4f20e76e33b"
# 39cb0: ASCII "d25f4db338e81b10"

# Juntos forman la clave de 256 bits
key_hex = 'ef39f4f20e76e33bd25f4db338e81b10'
key = bytes.fromhex(key_hex)

# Pero Salsa20 necesita 32 bytes, no 16
# Mirando más cuidadosamente el binario...

# Intentemos interpretar los datos crudos de .rodata
raw_at_39ca0 = bytes.fromhex('6566333966346632306537366533336264323566346462333338653831623130')
print(f"Raw data at 0x39ca0 (32 bytes): {raw_at_39ca0}")
print(f"As ASCII: {raw_at_39ca0.decode('ascii')}")

# Esto es "ef39f4f20e76e33bd25f4db338e81b10" - una cadena hex de 32 caracteres
# Que representa 16 bytes cuando se decodifica

# Tal vez la clave es interpretada diferente...
# El programa carga 32 bytes desde 0x39ca0 con dos instrucciones movaps/movdqa

# Intentemos usar los 32 bytes crudos como clave
key_32 = raw_at_39ca0
print(f"\nUsando clave de 32 bytes cruda: {key_32.hex()}")

# El nonce es "d4c270a3"
nonce = b'd4c270a3'

try:
    cipher = Salsa20.new(key=key_32, nonce=nonce)
    password = cipher.decrypt(expected)
    print(f"\nContraseña descifrada: {password}")
    
    # Verificar si es imprimible
    if all(32 <= b < 127 for b in password.rstrip(b'\x00\n')):
        password_str = password.decode('ascii').rstrip('\x00\n')
        print(f"¡CONTRASEÑA ENCONTRADA!: {password_str}")
        print(f"\nPrueba con: echo -n '{password_str}' | ./challenge/rauth")
except Exception as e:
    print(f"Error: {e}")

# Si eso no funciona, tal vez el nonce es diferente
print("\n\n=== Intentando con nonce del movabs directamente ===")
# movabs $0x3361303732633464 
nonce_raw = bytes.fromhex('3361303732633464')[::-1]  # little-endian
print(f"Nonce raw: {nonce_raw} ({nonce_raw.hex()})")

try:
    cipher2 = Salsa20.new(key=key_32, nonce=nonce_raw)
    password2 = cipher2.decrypt(expected)
    print(f"\nContraseña descifrada: {password2}")
    
    if all(32 <= b < 127 for b in password2.rstrip(b'\x00\n')):
        password_str2 = password2.decode('ascii').rstrip('\x00\n')
        print(f"¡CONTRASEÑA ENCONTRADA!: {password_str2}")
        print(f"\nPrueba con: echo -n '{password_str2}' | ./challenge/rauth")
except Exception as e:
    print(f"Error: {e}")