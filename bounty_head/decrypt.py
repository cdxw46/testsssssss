#!/usr/bin/env python3
import struct

# Contraseña hardcodeada desde el binario
password_bytes = bytearray()
password_hex = [
    0xf4, 0x98, 0x3a, 0x9a, 0x12, 0xa8, 0xf6, 0x12,
    0x12, 0xda, 0xaa, 0x12, 0x1a, 0xba, 0x14, 0x96
]

# Desencriptar la contraseña: (byte >> 1) ^ 0x39
decrypted_password = bytearray()
for byte in password_hex:
    decrypted = ((byte >> 1) ^ 0x39) & 0xFF
    decrypted_password.append(decrypted)

print(f"Contraseña desencriptada (hex): {decrypted_password.hex()}")
print(f"Contraseña desencriptada (ascii): {decrypted_password.decode('ascii', errors='replace')}")

# Leer efs.bin
with open('efs.bin', 'rb') as f:
    efs_data = f.read()

# Desencriptar efs.bin usando XOR con la contraseña (repitiendo la clave)
decrypted_efs = bytearray()
for i, byte in enumerate(efs_data):
    key_byte = decrypted_password[i % len(decrypted_password)]
    decrypted_byte = byte ^ key_byte
    decrypted_efs.append(decrypted_byte)

# Guardar el archivo desencriptado
with open('temp_03455.bin', 'wb') as f:
    f.write(decrypted_efs)

print(f"\nArchivo desencriptado guardado como temp_03455.bin")
print(f"Tamaño: {len(decrypted_efs)} bytes")
