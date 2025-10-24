#!/usr/bin/env python3

import base64
import re

def analyze_pattern():
    message = "=EDMxETMxEDMgATMxEDMwEDMgEDMxATMwEDMgATMxADMwEDMgETMxETMwEDMgEDMwETMwEDMgATMwATMwEDMgEDMwADMwEDMgATMxEDMwEDMgEDMwEDMwEDMgATMwADMwEDMgETMxETMwEDMgADMxADMwEDMgATMxEDMwEDMgEDMwADMwEDMgETMxETMwEDMgEDMxADMwEDMgETMwATMwEDMgATMwATMwEDMgADMwATMxADMgEDMxEDMwEDMgETMwETMxEDMgEDMxADMwEDMgADMxATMwEDMgETMxADMwEDMgATMxADMwEDM"
    
    # Remover el = del inicio
    if message.startswith('='):
        message = message[1:]
    
    # Agregar padding si es necesario
    if len(message) % 4 != 0:
        padding_needed = 4 - (len(message) % 4)
        message = message + '=' * padding_needed
    
    try:
        # Decodificar base64
        decoded_bytes = base64.b64decode(message)
        
        # Convertir a hexadecimal
        hex_string = decoded_bytes.hex()
        
        # Agrupar en pares de 2 caracteres (bytes)
        hex_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
        
        # Convertir a enteros
        int_values = [int(pair, 16) for pair in hex_pairs]
        
        print("Análisis detallado del patrón:")
        print("="*50)
        
        # Agrupar en tripletes (parece que cada 3 bytes forman un grupo)
        triplets = []
        for i in range(0, len(int_values), 3):
            if i + 2 < len(int_values):
                triplets.append(int_values[i:i+3])
        
        print(f"Número de tripletes: {len(triplets)}")
        print("\nTripletes encontrados:")
        for i, triplet in enumerate(triplets):
            print(f"{i:2d}: {triplet}")
        
        # Analizar el patrón de los tripletes
        print("\nAnálisis de patrones en tripletes:")
        
        # Buscar patrones comunes
        triplet_patterns = {}
        for triplet in triplets:
            pattern = tuple(triplet)
            if pattern in triplet_patterns:
                triplet_patterns[pattern] += 1
            else:
                triplet_patterns[pattern] = 1
        
        print("Patrones más comunes:")
        sorted_patterns = sorted(triplet_patterns.items(), key=lambda x: x[1], reverse=True)
        for pattern, count in sorted_patterns[:10]:
            print(f"  {pattern}: {count} veces")
        
        # Intentar interpretar como caracteres ASCII
        print("\nIntentando interpretar como caracteres ASCII:")
        ascii_interpretation = []
        for triplet in triplets:
            # Intentar diferentes interpretaciones
            # 1. Como caracteres individuales
            chars = [chr(val) if 32 <= val <= 126 else f'[{val}]' for val in triplet]
            ascii_interpretation.append(''.join(chars))
        
        print("Interpretación ASCII de tripletes:")
        for i, interpretation in enumerate(ascii_interpretation):
            print(f"{i:2d}: {interpretation}")
        
        # Buscar patrones que podrían ser texto
        all_text = ''.join(ascii_interpretation)
        print(f"\nTexto completo: {all_text}")
        
        # Buscar secuencias que podrían ser una flag
        flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', all_text)
        print(f"Posibles flags encontradas: {flag_patterns}")
        
        # Intentar interpretar los números como caracteres ASCII directamente
        print("\nIntentando interpretar números como ASCII directamente:")
        ascii_direct = []
        for val in int_values:
            if 32 <= val <= 126:
                ascii_direct.append(chr(val))
            else:
                ascii_direct.append(f'[{val}]')
        
        direct_text = ''.join(ascii_direct)
        print(f"Texto directo: {direct_text}")
        
        # Buscar patrones de flag en el texto directo
        direct_flags = re.findall(r'[A-Za-z0-9_]{5,}', direct_text)
        print(f"Flags en texto directo: {direct_flags}")
        
        # Analizar los valores únicos y sus frecuencias
        print("\nAnálisis de frecuencias de valores:")
        value_counts = {}
        for val in int_values:
            value_counts[val] = value_counts.get(val, 0) + 1
        
        sorted_values = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
        for val, count in sorted_values:
            char_repr = chr(val) if 32 <= val <= 126 else f'[{val}]'
            print(f"  {val:2d} ({char_repr}): {count:3d} veces")
        
        # Intentar interpretar como base64 de nuevo
        print("\nIntentando re-codificar como base64:")
        try:
            # Tomar solo los caracteres imprimibles y convertir de vuelta
            printable_values = [val for val in int_values if 32 <= val <= 126]
            printable_bytes = bytes(printable_values)
            print(f"Bytes imprimibles: {printable_bytes}")
            
            # Intentar decodificar como base64
            try:
                redecoded = base64.b64decode(printable_bytes)
                print(f"Re-decodificado: {redecoded}")
                print(f"Como texto: {redecoded.decode('utf-8', errors='ignore')}")
            except:
                print("No se pudo re-decodificar como base64")
                
        except Exception as e:
            print(f"Error en re-codificación: {e}")
        
        return triplets, ascii_interpretation
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    analyze_pattern()