#!/usr/bin/env python3

import base64
import re

def decode_message():
    message = "=EDMxETMxEDMgATMxEDMwEDMgEDMxATMwEDMgATMxADMwEDMgETMxETMwEDMgEDMwETMwEDMgATMwATMwEDMgEDMwADMwEDMgATMxEDMwEDMgEDMwEDMwEDMgATMwADMwEDMgETMxETMwEDMgADMxADMwEDMgATMxEDMwEDMgEDMwADMwEDMgETMxETMwEDMgEDMxADMwEDMgETMwATMwEDMgATMwATMwEDMgADMwATMxADMgEDMxEDMwEDMgETMwETMxEDMgEDMxADMwEDMgADMxATMwEDMgETMxADMwEDMgATMxADMwEDM"
    
    # Remover el = del inicio
    if message.startswith('='):
        message = message[1:]
    
    # Agregar padding si es necesario
    if len(message) % 4 != 0:
        padding_needed = 4 - (len(message) % 4)
        message = message + '=' * padding_needed
    
    print("Decodificando mensaje...")
    
    try:
        # Decodificar base64
        decoded_bytes = base64.b64decode(message)
        print(f"Bytes decodificados: {len(decoded_bytes)} bytes")
        
        # Convertir a hexadecimal para análisis
        hex_string = decoded_bytes.hex()
        print(f"Como hexadecimal: {hex_string}")
        
        # Agrupar en pares de 2 caracteres (bytes)
        hex_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
        print(f"Pares hexadecimales: {hex_pairs}")
        
        # Convertir a enteros
        int_values = [int(pair, 16) for pair in hex_pairs]
        print(f"Valores enteros: {int_values}")
        
        # Intentar interpretar como caracteres ASCII
        ascii_chars = []
        for val in int_values:
            if 32 <= val <= 126:  # Caracteres imprimibles
                ascii_chars.append(chr(val))
            else:
                ascii_chars.append(f'[{val}]')
        
        print(f"Como caracteres ASCII: {''.join(ascii_chars)}")
        
        # Intentar interpretar como texto
        try:
            text = ''.join([chr(val) for val in int_values if 32 <= val <= 126])
            print(f"Texto extraído: {text}")
        except:
            print("No se pudo convertir a texto legible")
        
        # Analizar patrones en los valores
        print(f"\nAnálisis de patrones:")
        print(f"Valores únicos: {sorted(set(int_values))}")
        print(f"Rango de valores: {min(int_values)} - {max(int_values)}")
        
        # Buscar patrones que podrían ser una flag
        flag_pattern = re.search(r'[A-Za-z0-9_]{10,}', ''.join(ascii_chars))
        if flag_pattern:
            print(f"Posible flag encontrada: {flag_pattern.group()}")
        
        # Intentar diferentes interpretaciones
        print(f"\nIntentando diferentes interpretaciones:")
        
        # 1. Como caracteres individuales
        chars = [chr(val) for val in int_values]
        print(f"1. Caracteres directos: {''.join(chars)}")
        
        # 2. Buscar secuencias que podrían ser texto
        text_chars = [chr(val) for val in int_values if 32 <= val <= 126]
        print(f"2. Solo caracteres imprimibles: {''.join(text_chars)}")
        
        # 3. Intentar con diferentes codificaciones
        try:
            utf8_text = decoded_bytes.decode('utf-8', errors='ignore')
            print(f"3. Como UTF-8: {utf8_text}")
        except:
            print("3. No se pudo decodificar como UTF-8")
        
        # 4. Buscar patrones de flag
        full_text = ''.join(chars)
        flag_matches = re.findall(r'[A-Za-z0-9_]{5,}', full_text)
        print(f"4. Posibles flags: {flag_matches}")
        
        return int_values, chars
        
    except Exception as e:
        print(f"Error en decodificación: {e}")
        return None, None

if __name__ == "__main__":
    decode_message()