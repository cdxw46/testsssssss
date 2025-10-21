#!/usr/bin/env python3
from Crypto.Cipher import Salsa20

# Datos extraídos del binario en las direcciones indicadas
# 0x39ca0: ef39f4f20e76e33bd25f4db338e81b10
# 0x39cb0: 65663339663466323065373665333362 (esto es "ef39f4f20e76e33b" en ASCII hex)

# La clave completa de 32 bytes se forma desde 0x39ca0
key_bytes = bytes.fromhex('ef39f4f20e76e33bd25f4db338e81b1065663339663466323065373665333362')

# Pero espera, la segunda parte parece ser hexadecimal en ASCII
# Decodifiquemos la segunda parte
second_part_hex = '65663339663466323065373665333362'
second_part_ascii = bytes.fromhex(second_part_hex).decode('ascii')
print(f"Segunda parte como ASCII: {second_part_ascii}")

# Ahora decodifiquemos ese hex ASCII a bytes
second_part_bytes = bytes.fromhex(second_part_ascii)

# La clave real es la primera parte + la segunda parte decodificada
key = bytes.fromhex('ef39f4f20e76e33bd25f4db338e81b10') + second_part_bytes
print(f"Key length: {len(key)}")
print(f"Key (hex): {key.hex()}")

# El nonce
nonce = bytes.fromhex('3361303732633464')  # "3a072c4d" en ASCII
print(f"Nonce: {nonce} ({nonce.hex()})")

# Los bytes esperados después del cifrado
expected = bytes.fromhex('05055fb1a329a8d558d9f556a6cb31f324432a31c99dec72e33eb66f62ad1bf9')

# Descifrar con Salsa20
cipher = Salsa20.new(key=key, nonce=nonce)
password = cipher.decrypt(expected)

print(f"\nPassword (raw): {password}")
print(f"Password (hex): {password.hex()}")

# Intentar decodificar como texto
try:
    password_text = password.decode('ascii').rstrip('\x00').rstrip('\n')
    print(f"Password (ASCII): {password_text}")
    
    # Si es una flag de HTB, probablemente empiece con HTB{
    if password_text.startswith('HTB{') or 'HTB{' in password_text:
        print(f"\n¡FLAG ENCONTRADA!: {password_text}")
except:
    print("No es ASCII directo, revisando si es la flag...")
    # A veces la flag está en el output después de ingresar la contraseña correcta
    print(f"\nPrueba esta contraseña (como hex): {password.hex()}")
    print(f"O estos bytes: {' '.join(f'{b:02x}' for b in password)}")