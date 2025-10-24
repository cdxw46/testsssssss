#!/usr/bin/env python3

import base64
import re

def pattern_decode():
    message = "=EDMxETMxEDMgATMxEDMwEDMgEDMxATMwEDMgATMxADMwEDMgETMxETMwEDMgEDMwETMwEDMgATMwATMwEDMgEDMwADMwEDMgATMxEDMwEDMgEDMwEDMwEDMgATMwADMwEDMgETMxETMwEDMgADMxADMwEDMgATMxEDMwEDMgEDMwADMwEDMgETMxETMwEDMgEDMxADMwEDMgETMwATMwEDMgATMwATMwEDMgADMwATMxADMgEDMxEDMwEDMgETMwETMxEDMgEDMxADMwEDMgADMxATMwEDMgETMxADMwEDMgATMxADMwEDM"
    
    # Remover el = del inicio
    if message.startswith('='):
        message = message[1:]
    
    print("Análisis del patrón de 4 caracteres:")
    print("="*50)
    
    # Analizar el patrón de 4 caracteres
    pattern = re.findall(r'.{4}', message)
    print(f"Número de patrones de 4 caracteres: {len(pattern)}")
    
    # Mostrar los primeros 20 patrones
    print("\nPrimeros 20 patrones:")
    for i, p in enumerate(pattern[:20]):
        print(f"{i:2d}: {p}")
    
    # Analizar los caracteres únicos
    unique_chars = set(message)
    print(f"\nCaracteres únicos: {sorted(unique_chars)}")
    
    # Crear un mapeo de caracteres a números
    char_to_num = {}
    for char in unique_chars:
        if char == 'E':
            char_to_num[char] = 0
        elif char == 'A':
            char_to_num[char] = 1
        elif char == 'D':
            char_to_num[char] = 2
        elif char == 'M':
            char_to_num[char] = 3
        elif char == 'T':
            char_to_num[char] = 4
        elif char == 'x':
            char_to_num[char] = 5
        elif char == 'g':
            char_to_num[char] = 6
        elif char == 'w':
            char_to_num[char] = 7
    
    print(f"\nMapeo de caracteres a números:")
    for char, num in char_to_num.items():
        print(f"  {char} -> {num}")
    
    # Convertir cada patrón de 4 caracteres a números
    print("\nConvirtiendo patrones a números:")
    numeric_patterns = []
    for p in pattern:
        numeric = [char_to_num[char] for char in p]
        numeric_patterns.append(numeric)
        print(f"{p} -> {numeric}")
    
    # Intentar interpretar como base 8
    print("\nIntentando interpretar como base 8:")
    base8_values = []
    for numeric in numeric_patterns:
        # Convertir a string y luego a base 8
        num_str = ''.join(map(str, numeric))
        try:
            base8_val = int(num_str, 8)
            base8_values.append(base8_val)
            print(f"{numeric} -> {num_str} -> {base8_val} -> {chr(base8_val) if 32 <= base8_val <= 126 else f'[{base8_val}]'}")
        except:
            print(f"{numeric} -> {num_str} -> Error")
    
    # Intentar interpretar como base 4
    print("\nIntentando interpretar como base 4:")
    base4_values = []
    for numeric in numeric_patterns:
        num_str = ''.join(map(str, numeric))
        try:
            base4_val = int(num_str, 4)
            base4_values.append(base4_val)
            print(f"{numeric} -> {num_str} -> {base4_val} -> {chr(base4_val) if 32 <= base4_val <= 126 else f'[{base4_val}]'}")
        except:
            print(f"{numeric} -> {num_str} -> Error")
    
    # Intentar interpretar como base 5
    print("\nIntentando interpretar como base 5:")
    base5_values = []
    for numeric in numeric_patterns:
        num_str = ''.join(map(str, numeric))
        try:
            base5_val = int(num_str, 5)
            base5_values.append(base5_val)
            print(f"{numeric} -> {num_str} -> {base5_val} -> {chr(base5_val) if 32 <= base5_val <= 126 else f'[{base5_val}]'}")
        except:
            print(f"{numeric} -> {num_str} -> Error")
    
    # Intentar interpretar como base 6
    print("\nIntentando interpretar como base 6:")
    base6_values = []
    for numeric in numeric_patterns:
        num_str = ''.join(map(str, numeric))
        try:
            base6_val = int(num_str, 6)
            base6_values.append(base6_val)
            print(f"{numeric} -> {num_str} -> {base6_val} -> {chr(base6_val) if 32 <= base6_val <= 126 else f'[{base6_val}]'}")
        except:
            print(f"{numeric} -> {num_str} -> Error")
    
    # Intentar interpretar como base 7
    print("\nIntentando interpretar como base 7:")
    base7_values = []
    for numeric in numeric_patterns:
        num_str = ''.join(map(str, numeric))
        try:
            base7_val = int(num_str, 7)
            base7_values.append(base7_val)
            print(f"{numeric} -> {num_str} -> {base7_val} -> {chr(base7_val) if 32 <= base7_val <= 126 else f'[{base7_val}]'}")
        except:
            print(f"{numeric} -> {num_str} -> Error")
    
    # Intentar interpretar como base 8 (otra vez, pero con mejor mapeo)
    print("\nIntentando mapeo diferente para base 8:")
    # Mapeo alternativo: E=0, A=1, D=2, M=3, T=4, x=5, g=6, w=7
    alt_char_to_num = {'E': 0, 'A': 1, 'D': 2, 'M': 3, 'T': 4, 'x': 5, 'g': 6, 'w': 7}
    
    alt_numeric_patterns = []
    for p in pattern:
        alt_numeric = [alt_char_to_num[char] for char in p]
        alt_numeric_patterns.append(alt_numeric)
    
    alt_base8_values = []
    for numeric in alt_numeric_patterns:
        num_str = ''.join(map(str, numeric))
        try:
            base8_val = int(num_str, 8)
            alt_base8_values.append(base8_val)
            print(f"{numeric} -> {num_str} -> {base8_val} -> {chr(base8_val) if 32 <= base8_val <= 126 else f'[{base8_val}]'}")
        except:
            print(f"{numeric} -> {num_str} -> Error")
    
    # Buscar patrones de flag en los resultados
    print("\nBuscando patrones de flag:")
    all_results = [base8_values, base4_values, base5_values, base6_values, base7_values, alt_base8_values]
    result_names = ['Base 8', 'Base 4', 'Base 5', 'Base 6', 'Base 7', 'Alt Base 8']
    
    for i, (values, name) in enumerate(zip(all_results, result_names)):
        if values:
            # Convertir a caracteres
            chars = []
            for val in values:
                if 32 <= val <= 126:
                    chars.append(chr(val))
                else:
                    chars.append(f'[{val}]')
            
            text = ''.join(chars)
            print(f"\n{name}: {text}")
            
            # Buscar patrones de flag
            flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', text)
            if flag_patterns:
                print(f"  Posibles flags: {flag_patterns}")
    
    return alt_base8_values

if __name__ == "__main__":
    pattern_decode()