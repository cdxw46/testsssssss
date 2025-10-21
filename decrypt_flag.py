#!/usr/bin/env python3
from Crypto.Cipher import Salsa20

# Después de la autenticación exitosa, el programa:
# 1. Carga datos desde 0x39cf0: 19397889 9768a08f 66d39017 b2e040c2
# 2. Carga un valor con movabs: 0x61e281c563371937
# 3. Aplica Salsa20 de nuevo

# Los datos a descifrar (24 bytes desde 0x39cf0 + movabs)
data_39cf0 = bytes.fromhex('193978899768a08f66d39017b2e040c2')  # 16 bytes
data_movabs = bytes.fromhex('61e281c563371937')[::-1]  # 8 bytes, little-endian

# Total 24 bytes
encrypted_flag = data_39cf0 + data_movabs
print(f"Encrypted flag data: {encrypted_flag.hex()} (len={len(encrypted_flag)})")

# La clave y nonce son los mismos que antes (se reutiliza el contexto Salsa20)
# Clave de 32 bytes
key = bytes.fromhex('6566333966346632306537366533336264323566346462333338653831623130')
nonce = b'd4c270a3'

# Crear nuevo cipher (el estado se reinicia)
cipher = Salsa20.new(key=key, nonce=nonce)

# Primero necesito avanzar el stream cipher por los 32 bytes de la contraseña
# ya que el contexto se reutiliza
password = b'TheCrucialRustEngineering@2021;)\n'
cipher.encrypt(password[:32])  # Avanzar el stream

# Ahora descifrar la flag
flag_bytes = cipher.decrypt(encrypted_flag)
print(f"\nFlag bytes: {flag_bytes}")
print(f"Flag hex: {flag_bytes.hex()}")

# Intentar decodificar
try:
    flag = flag_bytes.decode('ascii').rstrip('\x00')
    print(f"Flag decoded: {flag}")
    if 'HTB{' in flag:
        print(f"\n¡FLAG REAL ENCONTRADA!: {flag}")
except:
    print("No es ASCII directo")
    # Tal vez está en otro formato
    print("Flag como caracteres: ", end="")
    for b in flag_bytes:
        if 32 <= b < 127:
            print(chr(b), end="")
        else:
            print(f"\\x{b:02x}", end="")
    print()

# Otra posibilidad: el programa imprime "Flag: " y luego muestra algo
# Tal vez necesito ejecutar el programa completo
print("\n\nNOTA: La flag real puede estar en formato diferente.")
print("El programa muestra 'Flag: \"HTB{F4k3_f74g_4_t3s7ing}\"' que es una flag de prueba.")
print("La flag real podría estar en el servidor remoto o requerir interacción adicional.")