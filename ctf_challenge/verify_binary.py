#!/usr/bin/env python3

# Texto binario original
binary_text = "010000100110100101101110011000010111001001111001001000000100100101110100011100110010000001000100011010010110011101101001011101000110000101101100011010010110001101101001011011111110101011101000"

print(f"Longitud del texto binario: {len(binary_text)}")
print(f"¿Es divisible por 8? {len(binary_text) % 8 == 0}")

# Dividir en grupos de 8 bits
groups = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
print(f"Número de grupos: {len(groups)}")

# Mostrar cada grupo y su conversión
for i, group in enumerate(groups):
    if len(group) == 8:
        decimal = int(group, 2)
        char = chr(decimal)
        print(f"Grupo {i+1}: {group} -> {decimal} -> '{char}'")
    else:
        print(f"Grupo {i+1}: {group} (incompleto, {len(group)} bits)")

# Verificar si hay caracteres no imprimibles
print("\nVerificando caracteres no imprimables:")
for i, group in enumerate(groups):
    if len(group) == 8:
        decimal = int(group, 2)
        if decimal < 32 or decimal > 126:
            print(f"Grupo {i+1}: {group} -> {decimal} (no imprimible)")