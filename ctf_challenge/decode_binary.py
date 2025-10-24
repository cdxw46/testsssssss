#!/usr/bin/env python3

# Texto binario a decodificar
binary_text = "010000100110100101101110011000010111001001111001001000000100100101110100011100110010000001000100011010010110011101101001011101000110000101101100011010010110001101101001011011111110101011101000"

def binary_to_text(binary_string):
    # Dividir el string binario en grupos de 8 bits
    binary_groups = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    
    # Convertir cada grupo a su carácter ASCII correspondiente
    text = ""
    for group in binary_groups:
        if len(group) == 8:  # Asegurarse de que el grupo tenga 8 bits
            decimal = int(group, 2)
            text += chr(decimal)
    
    return text

# Decodificar el texto
decoded_text = binary_to_text(binary_text)
print(f"Texto decodificado: {decoded_text}")