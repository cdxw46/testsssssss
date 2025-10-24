#!/usr/bin/env python3

import base64
import re

def final_decode():
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
    
    print("Análisis final de decodificación:")
    print("="*50)
    
    # Intentar base 6 (más prometedor)
    print("1. Base 6 (más prometedor):")
    base6_chars = []
    for numeric in numeric_patterns:
        num_str = ''.join(map(str, numeric))
        try:
            base6_val = int(num_str, 6)
            if 32 <= base6_val <= 126:
                base6_chars.append(chr(base6_val))
            else:
                base6_chars.append(f'[{base6_val}]')
        except:
            base6_chars.append('?')
    
    base6_text = ''.join(base6_chars)
    print(f"Resultado base 6: {base6_text}")
    
    # Buscar patrones de flag en base 6
    flag_patterns_6 = re.findall(r'[A-Za-z0-9_]{5,}', base6_text)
    if flag_patterns_6:
        print(f"Posibles flags en base 6: {flag_patterns_6}")
    
    # Intentar base 7
    print("\n2. Base 7:")
    base7_chars = []
    for numeric in numeric_patterns:
        num_str = ''.join(map(str, numeric))
        try:
            base7_val = int(num_str, 7)
            if 32 <= base7_val <= 126:
                base7_chars.append(chr(base7_val))
            else:
                base7_chars.append(f'[{base7_val}]')
        except:
            base7_chars.append('?')
    
    base7_text = ''.join(base7_chars)
    print(f"Resultado base 7: {base7_text}")
    
    # Buscar patrones de flag en base 7
    flag_patterns_7 = re.findall(r'[A-Za-z0-9_]{5,}', base7_text)
    if flag_patterns_7:
        print(f"Posibles flags en base 7: {flag_patterns_7}")
    
    # Intentar base 8
    print("\n3. Base 8:")
    base8_chars = []
    for numeric in numeric_patterns:
        num_str = ''.join(map(str, numeric))
        try:
            base8_val = int(num_str, 8)
            if 32 <= base8_val <= 126:
                base8_chars.append(chr(base8_val))
            else:
                base8_chars.append(f'[{base8_val}]')
        except:
            base8_chars.append('?')
    
    base8_text = ''.join(base8_chars)
    print(f"Resultado base 8: {base8_text}")
    
    # Buscar patrones de flag en base 8
    flag_patterns_8 = re.findall(r'[A-Za-z0-9_]{5,}', base8_text)
    if flag_patterns_8:
        print(f"Posibles flags en base 8: {flag_patterns_8}")
    
    # Analizar los caracteres imprimibles de cada base
    print("\n4. Análisis de caracteres imprimibles:")
    
    for base_name, text in [("Base 6", base6_text), ("Base 7", base7_text), ("Base 8", base8_text)]:
        printable_chars = [c for c in text if c.isprintable() and c not in '[]?']
        printable_text = ''.join(printable_chars)
        print(f"{base_name}: {printable_text}")
        
        # Buscar patrones específicos
        if 'HTB' in printable_text.upper():
            print(f"  *** ENCONTRADO HTB en {base_name} ***")
        if 'CTF' in printable_text.upper():
            print(f"  *** ENCONTRADO CTF en {base_name} ***")
        if 'FLAG' in printable_text.upper():
            print(f"  *** ENCONTRADO FLAG en {base_name} ***")
    
    # Intentar interpretar como base64 después de la conversión
    print("\n5. Intentando decodificar como base64 después de conversión:")
    
    for base_name, text in [("Base 6", base6_text), ("Base 7", base7_text), ("Base 8", base8_text)]:
        # Tomar solo caracteres imprimibles
        clean_text = ''.join([c for c in text if c.isprintable() and c not in '[]?'])
        
        if len(clean_text) > 0:
            print(f"\n{base_name} limpio: {clean_text}")
            
            # Intentar decodificar como base64
            try:
                # Agregar padding si es necesario
                while len(clean_text) % 4 != 0:
                    clean_text += '='
                
                decoded = base64.b64decode(clean_text)
                print(f"  Decodificado como base64: {decoded}")
                print(f"  Como texto: {decoded.decode('utf-8', errors='ignore')}")
            except Exception as e:
                print(f"  Error en decodificación base64: {e}")
    
    # Buscar patrones de flag en todos los resultados
    print("\n6. Resumen de posibles flags:")
    all_texts = [base6_text, base7_text, base8_text]
    all_names = ["Base 6", "Base 7", "Base 8"]
    
    for text, name in zip(all_texts, all_names):
        # Buscar patrones que podrían ser flags
        patterns = re.findall(r'[A-Za-z0-9_]{5,}', text)
        if patterns:
            print(f"{name}: {patterns}")
        
        # Buscar patrones específicos de flag
        if 'HTB{' in text or 'htb{' in text:
            print(f"*** FLAG ENCONTRADA en {name}: {text} ***")
        if 'CTF{' in text or 'ctf{' in text:
            print(f"*** FLAG ENCONTRADA en {name}: {text} ***")
    
    return base6_text, base7_text, base8_text

if __name__ == "__main__":
    final_decode()