#!/usr/bin/env python3

# Texto binario original
binary_text = "010000100110100101101110011000010111001001111001001000000100100101110100011100110010000001000100011010010110011101101001011101000110000101101100011010010110001101101001011011111110101011101000"

print(f"Texto binario original: {binary_text}")
print(f"Longitud: {len(binary_text)} bits")
print(f"Longitud en bytes: {len(binary_text) // 8}")

# Verificar si los últimos grupos son válidos
last_groups = binary_text[-16:]  # Últimos 16 bits
print(f"Últimos 16 bits: {last_groups}")

# Intentar diferentes interpretaciones
print("\nIntentando diferentes interpretaciones:")

# 1. Solo los primeros 22 grupos (176 bits)
first_176 = binary_text[:176]
groups_22 = [first_176[i:i+8] for i in range(0, 176, 8)]
text_22 = ""
for group in groups_22:
    decimal = int(group, 2)
    text_22 += chr(decimal)
print(f"Primeros 22 grupos: '{text_22}'")

# 2. Verificar si hay padding o caracteres especiales
print(f"\nÚltimos 8 bits: {binary_text[-8:]}")
print(f"Últimos 8 bits como decimal: {int(binary_text[-8:], 2)}")

# 3. Verificar si es un mensaje completo
print(f"\n¿El mensaje parece completo? {text_22.endswith('o')}")