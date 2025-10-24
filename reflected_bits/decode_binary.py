#!/usr/bin/env python3

import base64
import re

def decode_binary():
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
        
        # Crear tripletes
        triplets = []
        for i in range(0, len(int_values), 3):
            if i + 2 < len(int_values):
                triplets.append(int_values[i:i+3])
        
        # Mapeo basado en el tercer valor del triplete
        binary_string = ""
        for triplet in triplets:
            if len(triplet) >= 3:
                if triplet[2] == 48:
                    binary_string += "0"
                elif triplet[2] == 49:
                    binary_string += "1"
                elif triplet[2] == 51:
                    binary_string += "3"
                elif triplet[2] == 32:
                    binary_string += " "
        
        print("Patrón binario extraído:")
        print(binary_string)
        print()
        
        # Remover espacios y analizar
        binary_clean = binary_string.replace(" ", "")
        print(f"Patrón binario sin espacios: {binary_clean}")
        print(f"Longitud: {len(binary_clean)}")
        
        # Intentar diferentes interpretaciones del patrón binario
        print("\nIntentando diferentes interpretaciones:")
        
        # 1. Como ASCII (8 bits por carácter)
        print("1. Interpretación ASCII (8 bits por carácter):")
        ascii_result = ""
        for i in range(0, len(binary_clean), 8):
            if i + 8 <= len(binary_clean):
                byte_str = binary_clean[i:i+8]
                try:
                    ascii_char = chr(int(byte_str, 2))
                    ascii_result += ascii_char
                except:
                    ascii_result += f"[{byte_str}]"
        
        print(f"Resultado ASCII: {ascii_result}")
        
        # 2. Como ASCII con diferentes longitudes de byte
        print("\n2. Intentando diferentes longitudes de byte:")
        for byte_len in [7, 6, 5, 4]:
            result = ""
            for i in range(0, len(binary_clean), byte_len):
                if i + byte_len <= len(binary_clean):
                    byte_str = binary_clean[i:i+byte_len]
                    try:
                        ascii_char = chr(int(byte_str, 2))
                        if ascii_char.isprintable():
                            result += ascii_char
                        else:
                            result += f"[{byte_str}]"
                    except:
                        result += f"[{byte_str}]"
            print(f"  {byte_len} bits: {result}")
        
        # 3. Buscar patrones que podrían ser una flag
        print("\n3. Buscando patrones de flag:")
        
        # Buscar secuencias que podrían ser flags
        flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', ascii_result)
        if flag_patterns:
            print(f"  Posibles flags en ASCII: {flag_patterns}")
        
        # Buscar en el patrón binario original (con espacios)
        print("\n4. Analizando el patrón con espacios:")
        binary_parts = binary_string.split()
        print(f"Partes del patrón: {binary_parts}")
        
        # Intentar interpretar cada parte como un carácter
        char_parts = []
        for part in binary_parts:
            if part in ['00', '01', '10', '11']:
                # Convertir a decimal
                decimal = int(part, 2)
                char_parts.append(str(decimal))
            else:
                char_parts.append(part)
        
        print(f"Partes como decimales: {char_parts}")
        
        # Intentar interpretar como caracteres ASCII
        ascii_parts = []
        for part in binary_parts:
            if part in ['00', '01', '10', '11']:
                decimal = int(part, 2)
                if 32 <= decimal <= 126:
                    ascii_parts.append(chr(decimal))
                else:
                    ascii_parts.append(f"[{decimal}]")
            else:
                ascii_parts.append(part)
        
        print(f"Partes como ASCII: {ascii_parts}")
        
        # 5. Intentar interpretar como base64
        print("\n5. Intentando interpretar como base64:")
        try:
            # Tomar solo los caracteres imprimibles del resultado ASCII
            printable_ascii = ''.join([c for c in ascii_result if c.isprintable()])
            print(f"ASCII imprimible: {printable_ascii}")
            
            # Intentar decodificar como base64
            try:
                base64_decoded = base64.b64decode(printable_ascii)
                print(f"Decodificado como base64: {base64_decoded}")
                print(f"Como texto: {base64_decoded.decode('utf-8', errors='ignore')}")
            except:
                print("No se pudo decodificar como base64")
        except Exception as e:
            print(f"Error: {e}")
        
        # 6. Buscar patrones específicos de flag
        print("\n6. Buscando patrones específicos de flag:")
        
        # Buscar patrones que empiecen con letras comunes de flags
        flag_starts = ['HTB', 'CTF', 'FLAG', 'flag', 'Flag']
        for start in flag_starts:
            if start.lower() in ascii_result.lower():
                print(f"  Encontrado patrón que empieza con {start}")
        
        # Buscar en el patrón binario original
        original_pattern = binary_string.replace(" ", "")
        print(f"\nPatrón binario completo: {original_pattern}")
        
        # Intentar diferentes agrupaciones
        print("\n7. Intentando diferentes agrupaciones del patrón binario:")
        
        # Agrupar de 2 en 2
        pairs = [original_pattern[i:i+2] for i in range(0, len(original_pattern), 2)]
        print(f"Pares: {pairs}")
        
        # Convertir pares a caracteres
        pair_chars = []
        for pair in pairs:
            if len(pair) == 2:
                decimal = int(pair, 2)
                if 32 <= decimal <= 126:
                    pair_chars.append(chr(decimal))
                else:
                    pair_chars.append(f"[{decimal}]")
            else:
                pair_chars.append(pair)
        
        print(f"Pares como caracteres: {''.join(pair_chars)}")
        
        return ascii_result, pair_chars
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    decode_binary()