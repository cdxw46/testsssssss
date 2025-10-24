#!/usr/bin/env python3

import base64
import re

def binary_analysis():
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
        
        print("Análisis de codificación binaria:")
        print("="*50)
        
        # Mapear valores a caracteres binarios
        # Basándome en el análisis anterior:
        # 51 = '3' (más frecuente)
        # 48 = '0' 
        # 49 = '1'
        # 32 = ' ' (espacio)
        # 16, 17, 0, 1 parecen ser delimitadores o marcadores
        
        # Crear un mapeo basado en los patrones observados
        binary_map = {}
        
        # Analizar tripletes para entender el patrón
        triplets = []
        for i in range(0, len(int_values), 3):
            if i + 2 < len(int_values):
                triplets.append(int_values[i:i+3])
        
        print("Análisis de tripletes para mapeo binario:")
        
        # Buscar patrones que podrían representar 0 y 1
        # El patrón más común es (16, 51, 32) que aparece 24 veces
        # Esto podría ser un delimitador o separador
        
        # Intentar diferentes mapeos
        print("\nIntentando mapeo 1: 48='0', 49='1'")
        binary_string_1 = ""
        for val in int_values:
            if val == 48:
                binary_string_1 += "0"
            elif val == 49:
                binary_string_1 += "1"
            elif val == 32:
                binary_string_1 += " "  # Espacio
            elif val == 51:
                binary_string_1 += "3"  # Delimitador?
        
        print(f"Resultado: {binary_string_1}")
        
        # Intentar mapeo 2: basado en posición en el triplete
        print("\nIntentando mapeo 2: basado en posición en tripletes")
        binary_string_2 = ""
        for triplet in triplets:
            # El primer valor podría ser un marcador, el segundo el valor real
            if len(triplet) >= 2:
                if triplet[1] == 48:
                    binary_string_2 += "0"
                elif triplet[1] == 49:
                    binary_string_2 += "1"
                elif triplet[1] == 51:
                    binary_string_2 += "3"
        
        print(f"Resultado: {binary_string_2}")
        
        # Intentar mapeo 3: basado en el tercer valor del triplete
        print("\nIntentando mapeo 3: basado en tercer valor de tripletes")
        binary_string_3 = ""
        for triplet in triplets:
            if len(triplet) >= 3:
                if triplet[2] == 48:
                    binary_string_3 += "0"
                elif triplet[2] == 49:
                    binary_string_3 += "1"
                elif triplet[2] == 51:
                    binary_string_3 += "3"
                elif triplet[2] == 32:
                    binary_string_3 += " "
        
        print(f"Resultado: {binary_string_3}")
        
        # Intentar mapeo 4: basado en el primer valor del triplete
        print("\nIntentando mapeo 4: basado en primer valor de tripletes")
        binary_string_4 = ""
        for triplet in triplets:
            if len(triplet) >= 1:
                if triplet[0] == 48:
                    binary_string_4 += "0"
                elif triplet[0] == 49:
                    binary_string_4 += "1"
                elif triplet[0] == 51:
                    binary_string_4 += "3"
                elif triplet[0] == 32:
                    binary_string_4 += " "
        
        print(f"Resultado: {binary_string_4}")
        
        # Intentar mapeo 5: combinación de valores
        print("\nIntentando mapeo 5: combinación de valores")
        binary_string_5 = ""
        for triplet in triplets:
            if len(triplet) >= 3:
                # Usar el segundo valor como el bit principal
                if triplet[1] == 48:
                    binary_string_5 += "0"
                elif triplet[1] == 49:
                    binary_string_5 += "1"
                # Usar el tercer valor para espacios
                if triplet[2] == 32:
                    binary_string_5 += " "
        
        print(f"Resultado: {binary_string_5}")
        
        # Buscar patrones de flag en todos los mapeos
        print("\nBuscando patrones de flag en todos los mapeos:")
        all_strings = [binary_string_1, binary_string_2, binary_string_3, binary_string_4, binary_string_5]
        
        for i, binary_str in enumerate(all_strings, 1):
            print(f"\nMapeo {i}:")
            print(f"  Longitud: {len(binary_str)}")
            
            # Buscar patrones que podrían ser flags
            flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', binary_str)
            if flag_patterns:
                print(f"  Posibles flags: {flag_patterns}")
            
            # Buscar patrones binarios que podrían decodificarse
            binary_patterns = re.findall(r'[01]+', binary_str)
            if binary_patterns:
                print(f"  Patrones binarios: {binary_patterns[:10]}...")  # Mostrar solo los primeros 10
                
                # Intentar decodificar algunos patrones binarios
                for pattern in binary_patterns[:5]:  # Solo los primeros 5
                    if len(pattern) % 8 == 0:  # Múltiplo de 8 bits
                        try:
                            # Convertir a bytes y luego a texto
                            bytes_data = int(pattern, 2).to_bytes(len(pattern) // 8, byteorder='big')
                            text = bytes_data.decode('utf-8', errors='ignore')
                            if text.isprintable():
                                print(f"    {pattern} -> {text}")
                        except:
                            pass
        
        return binary_string_5  # Retornar el mapeo más prometedor
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    binary_analysis()