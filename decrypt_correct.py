#!/usr/bin/env python3
from Crypto.Cipher import Salsa20

# Los datos en rodata son strings ASCII que representan hexadecimal
# 0x39ca0: "ef39f4f20e76e33b" (ASCII)
# 0x39cb0: "d25f4db338e81b10" (ASCII)

# Leer como bytes ASCII primero
key_part1_ascii = bytes.fromhex('65663339663466323065373665333362').decode('ascii')  # "ef39f4f20e76e33b"
key_part2_ascii = bytes.fromhex('64323566346462333338653831623130').decode('ascii')  # "d25f4db338e81b10"

print(f"Key part 1 (ASCII): {key_part1_ascii}")
print(f"Key part 2 (ASCII): {key_part2_ascii}")

# Combinar las dos partes del string hexadecimal
key_hex_string = key_part1_ascii + key_part2_ascii
print(f"Key hex string: {key_hex_string}")

# Convertir el string hexadecimal a bytes
key = bytes.fromhex(key_hex_string)
print(f"Key (32 bytes): {key.hex()}")
print(f"Key length: {len(key)}")

# El nonce - también es ASCII "3a072c4d"
nonce_ascii = bytes.fromhex('3361303732633464').decode('ascii')  # "3a072c4d"
print(f"Nonce (ASCII): {nonce_ascii}")
nonce = bytes.fromhex(nonce_ascii)
print(f"Nonce (bytes): {nonce.hex()}")

# Los bytes esperados después del cifrado
expected = bytes.fromhex('05055fb1a329a8d558d9f556a6cb31f324432a31c99dec72e33eb66f62ad1bf9')

# Descifrar con Salsa20
cipher = Salsa20.new(key=key, nonce=nonce)
password = cipher.decrypt(expected)

print(f"\n=== RESULTADO ===")
print(f"Password (bytes): {password}")
print(f"Password (hex): {password.hex()}")

# Intentar como ASCII
try:
    # Eliminar posibles nulls o newlines al final
    password_clean = password.rstrip(b'\x00').rstrip(b'\n')
    password_text = password_clean.decode('ascii')
    print(f"Password (ASCII): {password_text}")
    print(f"Password length: {len(password_clean)}")
except:
    print("No es ASCII puro")

# Verificar con el binario
print(f"\nPara verificar, ejecuta:")
print(f"echo -n '{password_clean.decode('ascii', errors='ignore')}' | ./challenge/rauth")