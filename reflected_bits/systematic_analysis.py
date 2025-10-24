#!/usr/bin/env python3

import base64
import re

def systematic_analysis():
    message = "=EDMxETMxEDMgATMxEDMwEDMgEDMxATMwEDMgATMxADMwEDMgETMxETMwEDMgEDMwETMwEDMgATMwATMwEDMgEDMwADMwEDMgATMxEDMwEDMgEDMwEDMwEDMgATMwADMwEDMgETMxETMwEDMgADMxADMwEDMgATMxEDMwEDMgEDMwADMwEDMgETMxETMwEDMgEDMxADMwEDMgETMwATMwEDMgATMwATMwEDMgADMwATMxADMgEDMxEDMwEDMgETMwETMxEDMgEDMxADMwEDMgADMxATMwEDMgETMxADMwEDMgATMxADMwEDM"
    
    # Remover el = del inicio
    if message.startswith('='):
        message = message[1:]
    
    print("Análisis sistemático del mensaje:")
    print("="*50)
    
    # Analizar el patrón de 4 caracteres
    pattern = re.findall(r'.{4}', message)
    print(f"Número de patrones: {len(pattern)}")
    
    # Mostrar algunos patrones
    print(f"Primeros 10 patrones: {pattern[:10]}")
    
    # Analizar los caracteres únicos
    unique_chars = set(message)
    print(f"Caracteres únicos: {sorted(unique_chars)}")
    
    # Crear un mapeo diferente
    # Basándome en el análisis anterior, voy a probar un mapeo diferente
    char_mappings = [
        {'E': 0, 'A': 1, 'D': 2, 'M': 3, 'T': 4, 'x': 5, 'g': 6, 'w': 7},
        {'E': 1, 'A': 2, 'D': 3, 'M': 4, 'T': 5, 'x': 6, 'g': 7, 'w': 8},
        {'E': 0, 'A': 1, 'D': 2, 'M': 3, 'T': 4, 'x': 5, 'g': 6, 'w': 7},
    ]
    
    for i, char_map in enumerate(char_mappings):
        print(f"\n--- Mapeo {i+1}: {char_map} ---")
        
        # Convertir patrones a números
        numeric_patterns = []
        for p in pattern:
            try:
                numeric = [char_map[char] for char in p]
                numeric_patterns.append(numeric)
            except KeyError:
                print(f"Error: carácter no encontrado en {p}")
                break
        
        if not numeric_patterns:
            continue
        
        # Intentar diferentes bases
        for base in [6, 7, 8, 9, 10]:
            print(f"\n  Base {base}:")
            chars = []
            for numeric in numeric_patterns:
                num_str = ''.join(map(str, numeric))
                try:
                    val = int(num_str, base)
                    if 32 <= val <= 126:
                        chars.append(chr(val))
                    else:
                        chars.append(f'[{val}]')
                except:
                    chars.append('?')
            
            text = ''.join(chars)
            print(f"    Resultado: {text}")
            
            # Buscar patrones de flag
            flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', text)
            if flag_patterns:
                print(f"    *** Posibles flags: {flag_patterns} ***")
            
            # Buscar patrones específicos
            if 'HTB' in text.upper() or 'CTF' in text.upper() or 'FLAG' in text.upper():
                print(f"    *** PATRÓN DE FLAG ENCONTRADO: {text} ***")
    
    # Intentar un enfoque diferente: analizar el patrón como base64 directamente
    print(f"\n--- Enfoque alternativo: Base64 directo ---")
    
    # Agregar padding si es necesario
    if len(message) % 4 != 0:
        padding_needed = 4 - (len(message) % 4)
        message_padded = message + '=' * padding_needed
    else:
        message_padded = message
    
    print(f"Mensaje con padding: {message_padded}")
    
    try:
        decoded = base64.b64decode(message_padded)
        print(f"Decodificado: {decoded}")
        print(f"Como texto: {decoded.decode('utf-8', errors='ignore')}")
        
        # Buscar patrones de flag en el resultado
        flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', decoded.decode('utf-8', errors='ignore'))
        if flag_patterns:
            print(f"*** Posibles flags: {flag_patterns} ***")
            
    except Exception as e:
        print(f"Error en decodificación base64: {e}")
    
    # Intentar interpretar como hexadecimal
    print(f"\n--- Enfoque hexadecimal ---")
    
    # Convertir cada patrón de 4 caracteres a hexadecimal
    hex_patterns = []
    for p in pattern:
        # Convertir cada carácter a su valor ASCII
        ascii_vals = [ord(c) for c in p]
        hex_str = ''.join([f'{val:02x}' for val in ascii_vals])
        hex_patterns.append(hex_str)
    
    print(f"Patrones hexadecimales: {hex_patterns[:10]}...")
    
    # Intentar decodificar como hexadecimal
    try:
        hex_string = ''.join(hex_patterns)
        hex_bytes = bytes.fromhex(hex_string)
        print(f"Bytes hexadecimales: {hex_bytes}")
        print(f"Como texto: {hex_bytes.decode('utf-8', errors='ignore')}")
        
        # Buscar patrones de flag
        flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', hex_bytes.decode('utf-8', errors='ignore'))
        if flag_patterns:
            print(f"*** Posibles flags: {flag_patterns} ***")
            
    except Exception as e:
        print(f"Error en decodificación hexadecimal: {e}")
    
    return pattern

if __name__ == "__main__":
    systematic_analysis()