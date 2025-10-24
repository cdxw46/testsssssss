#!/usr/bin/env python3

import base64
import re

def hebrew_analysis():
    message = "=EDMxETMxEDMgATMxEDMwEDMgEDMxATMwEDMgATMxADMwEDMgETMxETMwEDMgEDMwETMwEDMgATMwATMwEDMgEDMwADMwEDMgATMxEDMwEDMgEDMwEDMwEDMgATMwADMwEDMgETMxETMwEDMgADMxADMwEDMgATMxEDMwEDMgEDMwADMwEDMgETMxETMwEDMgEDMxADMwEDMgETMwATMwEDMgATMwATMwEDMgADMwATMxADMgEDMxEDMwEDMgETMwETMxEDMgEDMxADMwEDMgADMxATMwEDMgETMxADMwEDMgATMxADMwEDM"
    
    # Remover el = del inicio
    if message.startswith('='):
        message = message[1:]
    
    # Analizar el patrón de 4 caracteres
    pattern = re.findall(r'.{4}', message)
    
    # Mapeo de caracteres a números
    char_to_num = {'E': 0, 'A': 1, 'D': 2, 'M': 3, 'T': 4, 'x': 5, 'g': 6, 'w': 7}
    
    # Convertir cada patrón de 4 caracteres a números
    numeric_patterns = []
    for p in pattern:
        numeric = [char_to_num[char] for char in p]
        numeric_patterns.append(numeric)
    
    print("Análisis del texto hebreo:")
    print("="*50)
    
    # Convertir a base 8 y luego a base64
    base8_values = []
    for numeric in numeric_patterns:
        num_str = ''.join(map(str, numeric))
        try:
            base8_val = int(num_str, 8)
            base8_values.append(base8_val)
        except:
            base8_values.append(0)
    
    # Convertir a bytes (solo valores válidos)
    valid_bytes = [val for val in base8_values if 0 <= val <= 255]
    base8_bytes = bytes(valid_bytes)
    print(f"Bytes válidos en base 8: {base8_bytes}")
    print(f"Valores fuera de rango: {[val for val in base8_values if val > 255]}")
    
    # Convertir a base64
    base64_encoded = base64.b64encode(base8_bytes).decode('utf-8')
    print(f"Codificado en base64: {base64_encoded}")
    
    # Decodificar de vuelta
    try:
        decoded = base64.b64decode(base64_encoded)
        print(f"Decodificado: {decoded}")
        print(f"Como texto: {decoded.decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"Error en decodificación: {e}")
    
    # Intentar diferentes interpretaciones
    print("\nIntentando diferentes interpretaciones:")
    
    # 1. Como caracteres ASCII individuales
    ascii_chars = []
    for val in base8_values:
        if 32 <= val <= 126:
            ascii_chars.append(chr(val))
        else:
            ascii_chars.append(f'[{val}]')
    
    ascii_text = ''.join(ascii_chars)
    print(f"1. Como ASCII: {ascii_text}")
    
    # 2. Buscar patrones en el texto hebreo
    hebrew_text = "מy{ןuy}ן;^|vy^}}ן5^|y^}ןuן6^|z]y{ןuyן6^|מ]yo;u}ן:^מyo;uyן:^|z]y{"
    print(f"\n2. Texto hebreo: {hebrew_text}")
    
    # Buscar patrones que podrían ser flags
    flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', hebrew_text)
    if flag_patterns:
        print(f"Patrones de flag en hebreo: {flag_patterns}")
    
    # 3. Intentar interpretar los bytes como diferentes codificaciones
    print("\n3. Intentando diferentes codificaciones de bytes:")
    
    # Como UTF-8
    try:
        utf8_text = base8_bytes.decode('utf-8', errors='ignore')
        print(f"UTF-8: {utf8_text}")
    except:
        print("UTF-8: Error")
    
    # Como Latin-1
    try:
        latin1_text = base8_bytes.decode('latin-1', errors='ignore')
        print(f"Latin-1: {latin1_text}")
    except:
        print("Latin-1: Error")
    
    # 4. Buscar patrones específicos
    print("\n4. Buscando patrones específicos:")
    
    # Buscar en el texto ASCII
    if 'HTB' in ascii_text.upper():
        print(f"*** ENCONTRADO HTB en ASCII: {ascii_text} ***")
    if 'CTF' in ascii_text.upper():
        print(f"*** ENCONTRADO CTF en ASCII: {ascii_text} ***")
    if 'FLAG' in ascii_text.upper():
        print(f"*** ENCONTRADO FLAG en ASCII: {ascii_text} ***")
    
    # Buscar en el texto hebreo
    if 'HTB' in hebrew_text.upper():
        print(f"*** ENCONTRADO HTB en hebreo: {hebrew_text} ***")
    if 'CTF' in hebrew_text.upper():
        print(f"*** ENCONTRADO CTF en hebreo: {hebrew_text} ***")
    if 'FLAG' in hebrew_text.upper():
        print(f"*** ENCONTRADO FLAG en hebreo: {hebrew_text} ***")
    
    # 5. Intentar interpretar como base64 de nuevo
    print("\n5. Intentando re-codificar como base64:")
    
    # Tomar solo caracteres imprimibles del texto ASCII
    printable_ascii = ''.join([c for c in ascii_text if c.isprintable() and c not in '[]'])
    print(f"ASCII imprimible: {printable_ascii}")
    
    # Intentar decodificar como base64
    try:
        # Agregar padding si es necesario
        while len(printable_ascii) % 4 != 0:
            printable_ascii += '='
        
        redecoded = base64.b64decode(printable_ascii)
        print(f"Re-decodificado: {redecoded}")
        print(f"Como texto: {redecoded.decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"Error en re-decodificación: {e}")
    
    # 6. Analizar los valores numéricos
    print("\n6. Análisis de valores numéricos:")
    print(f"Valores únicos: {sorted(set(base8_values))}")
    print(f"Rango: {min(base8_values)} - {max(base8_values)}")
    
    # Buscar patrones en los valores
    print(f"Primeros 20 valores: {base8_values[:20]}")
    
    # Intentar interpretar como caracteres ASCII directamente
    direct_ascii = ''.join([chr(val) for val in base8_values if 32 <= val <= 126])
    print(f"ASCII directo: {direct_ascii}")
    
    # Buscar patrones de flag en ASCII directo
    direct_flags = re.findall(r'[A-Za-z0-9_]{5,}', direct_ascii)
    if direct_flags:
        print(f"Flags en ASCII directo: {direct_flags}")
    
    return ascii_text, hebrew_text, direct_ascii

if __name__ == "__main__":
    hebrew_analysis()