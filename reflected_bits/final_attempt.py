#!/usr/bin/env python3

import base64
import re

def final_attempt():
    message = "=EDMxETMxEDMgATMxEDMwEDMgEDMxATMwEDMgATMxADMwEDMgETMxETMwEDMgEDMwETMwEDMgATMwATMwEDMgEDMwADMwEDMgATMxEDMwEDMgEDMwEDMwEDMgATMwADMwEDMgETMxETMwEDMgADMxADMwEDMgATMxEDMwEDMgEDMwADMwEDMgETMxETMwEDMgEDMxADMwEDMgETMwATMwEDMgATMwATMwEDMgADMwATMxADMgEDMxEDMwEDMgETMwETMxEDMgEDMxADMwEDMgADMxATMwEDMgETMxADMwEDMgATMxADMwEDM"
    
    print("Análisis final del mensaje:")
    print("="*50)
    
    # Remover el = del inicio
    if message.startswith('='):
        message = message[1:]
    
    print(f"Mensaje sin =: {message}")
    print(f"Longitud: {len(message)}")
    
    # Analizar el patrón de 4 caracteres
    pattern = re.findall(r'.{4}', message)
    print(f"Número de patrones de 4 caracteres: {len(pattern)}")
    
    # Mostrar algunos patrones
    print(f"Primeros 10 patrones: {pattern[:10]}")
    
    # Analizar los caracteres únicos
    unique_chars = set(message)
    print(f"Caracteres únicos: {sorted(unique_chars)}")
    
    # Intentar interpretar como base64 directamente
    print(f"\n--- Intentando base64 directo ---")
    
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
        
        # Buscar patrones de flag
        flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', decoded.decode('utf-8', errors='ignore'))
        if flag_patterns:
            print(f"*** Posibles flags: {flag_patterns} ***")
            
    except Exception as e:
        print(f"Error en decodificación base64: {e}")
    
    # Intentar interpretar como base32
    print(f"\n--- Intentando base32 ---")
    
    try:
        import base64
        # Convertir a base32
        base32_encoded = base64.b32encode(message.encode()).decode()
        print(f"Codificado en base32: {base32_encoded}")
        
        # Decodificar
        base32_decoded = base64.b32decode(base32_encoded)
        print(f"Decodificado: {base32_decoded}")
        print(f"Como texto: {base32_decoded.decode('utf-8', errors='ignore')}")
        
    except Exception as e:
        print(f"Error en base32: {e}")
    
    # Intentar interpretar como base16 (hexadecimal)
    print(f"\n--- Intentando base16 (hexadecimal) ---")
    
    try:
        # Convertir cada carácter a su valor hexadecimal
        hex_string = message.encode().hex()
        print(f"Como hexadecimal: {hex_string}")
        
        # Decodificar
        hex_decoded = bytes.fromhex(hex_string)
        print(f"Decodificado: {hex_decoded}")
        print(f"Como texto: {hex_decoded.decode('utf-8', errors='ignore')}")
        
    except Exception as e:
        print(f"Error en hexadecimal: {e}")
    
    # Intentar interpretar como base85
    print(f"\n--- Intentando base85 ---")
    
    try:
        import base64
        # Convertir a base85
        base85_encoded = base64.b85encode(message.encode()).decode()
        print(f"Codificado en base85: {base85_encoded}")
        
        # Decodificar
        base85_decoded = base64.b85decode(base85_encoded)
        print(f"Decodificado: {base85_decoded}")
        print(f"Como texto: {base85_decoded.decode('utf-8', errors='ignore')}")
        
    except Exception as e:
        print(f"Error en base85: {e}")
    
    # Intentar interpretar como base64 con diferentes caracteres
    print(f"\n--- Intentando base64 con mapeo de caracteres ---")
    
    # Crear un mapeo de caracteres
    char_map = {
        'E': 'A', 'D': 'B', 'M': 'C', 'x': 'D',
        'A': 'E', 'T': 'F', 'g': 'G', 'w': 'H'
    }
    
    # Mapear caracteres
    mapped_message = ''.join([char_map.get(c, c) for c in message])
    print(f"Mensaje mapeado: {mapped_message}")
    
    # Agregar padding si es necesario
    if len(mapped_message) % 4 != 0:
        padding_needed = 4 - (len(mapped_message) % 4)
        mapped_message_padded = mapped_message + '=' * padding_needed
    else:
        mapped_message_padded = mapped_message
    
    try:
        decoded = base64.b64decode(mapped_message_padded)
        print(f"Decodificado: {decoded}")
        print(f"Como texto: {decoded.decode('utf-8', errors='ignore')}")
        
        # Buscar patrones de flag
        flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', decoded.decode('utf-8', errors='ignore'))
        if flag_patterns:
            print(f"*** Posibles flags: {flag_patterns} ***")
            
    except Exception as e:
        print(f"Error en decodificación base64 mapeada: {e}")
    
    # Intentar interpretar como base64 con mapeo inverso
    print(f"\n--- Intentando base64 con mapeo inverso ---")
    
    # Crear un mapeo inverso de caracteres
    reverse_char_map = {
        'A': 'E', 'B': 'D', 'C': 'M', 'D': 'x',
        'E': 'A', 'F': 'T', 'G': 'g', 'H': 'w'
    }
    
    # Mapear caracteres
    reverse_mapped_message = ''.join([reverse_char_map.get(c, c) for c in message])
    print(f"Mensaje mapeado inverso: {reverse_mapped_message}")
    
    # Agregar padding si es necesario
    if len(reverse_mapped_message) % 4 != 0:
        padding_needed = 4 - (len(reverse_mapped_message) % 4)
        reverse_mapped_message_padded = reverse_mapped_message + '=' * padding_needed
    else:
        reverse_mapped_message_padded = reverse_mapped_message
    
    try:
        decoded = base64.b64decode(reverse_mapped_message_padded)
        print(f"Decodificado: {decoded}")
        print(f"Como texto: {decoded.decode('utf-8', errors='ignore')}")
        
        # Buscar patrones de flag
        flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', decoded.decode('utf-8', errors='ignore'))
        if flag_patterns:
            print(f"*** Posibles flags: {flag_patterns} ***")
            
    except Exception as e:
        print(f"Error en decodificación base64 mapeada inversa: {e}")
    
    # Intentar interpretar como base64 con mapeo numérico
    print(f"\n--- Intentando base64 con mapeo numérico ---")
    
    # Crear un mapeo numérico de caracteres
    num_char_map = {
        'E': '0', 'D': '1', 'M': '2', 'x': '3',
        'A': '4', 'T': '5', 'g': '6', 'w': '7'
    }
    
    # Mapear caracteres
    num_mapped_message = ''.join([num_char_map.get(c, c) for c in message])
    print(f"Mensaje mapeado numérico: {num_mapped_message}")
    
    # Agregar padding si es necesario
    if len(num_mapped_message) % 4 != 0:
        padding_needed = 4 - (len(num_mapped_message) % 4)
        num_mapped_message_padded = num_mapped_message + '=' * padding_needed
    else:
        num_mapped_message_padded = num_mapped_message
    
    try:
        decoded = base64.b64decode(num_mapped_message_padded)
        print(f"Decodificado: {decoded}")
        print(f"Como texto: {decoded.decode('utf-8', errors='ignore')}")
        
        # Buscar patrones de flag
        flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', decoded.decode('utf-8', errors='ignore'))
        if flag_patterns:
            print(f"*** Posibles flags: {flag_patterns} ***")
            
    except Exception as e:
        print(f"Error en decodificación base64 mapeada numérica: {e}")
    
    return message

if __name__ == "__main__":
    final_attempt()