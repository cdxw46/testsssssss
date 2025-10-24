#!/usr/bin/env python3

import base64
import re
from collections import Counter

def substitution_cipher():
    message = "=EDMxETMxEDMgATMxEDMwEDMgEDMxATMwEDMgATMxADMwEDMgETMxETMwEDMgEDMwETMwEDMgATMwATMwEDMgEDMwADMwEDMgATMxEDMwEDMgEDMwEDMwEDMgATMwADMwEDMgETMxETMwEDMgADMxADMwEDMgATMxEDMwEDMgEDMwADMwEDMgETMxETMwEDMgEDMxADMwEDMgETMwATMwEDMgATMwATMwEDMgADMwATMxADMgEDMxEDMwEDMgETMwETMxEDMgEDMxADMwEDMgADMxATMwEDMgETMxADMwEDMgATMxADMwEDM"
    
    # Remover el = del inicio
    if message.startswith('='):
        message = message[1:]
    
    print("Análisis de cifrado de sustitución:")
    print("="*50)
    
    # Analizar frecuencia de caracteres
    char_freq = Counter(message)
    print(f"Frecuencia de caracteres: {dict(char_freq)}")
    
    # Analizar frecuencia de patrones de 4 caracteres
    pattern = re.findall(r'.{4}', message)
    pattern_freq = Counter(pattern)
    print(f"Frecuencia de patrones (top 10): {dict(pattern_freq.most_common(10))}")
    
    # Intentar diferentes mapeos de sustitución
    print(f"\n--- Intentando mapeos de sustitución ---")
    
    # Mapeo 1: Basado en frecuencia
    # Los caracteres más frecuentes podrían ser espacios o letras comunes
    freq_order = [char for char, count in char_freq.most_common()]
    print(f"Orden por frecuencia: {freq_order}")
    
    # Mapeo 1: E=espacio, M=e, D=t, A=a, T=o, x=n, g=i, w=r
    mapping1 = {
        'E': ' ',  # Más frecuente
        'M': 'e',  # Segunda más frecuente
        'D': 't',  # Tercera más frecuente
        'A': 'a',  # Cuarta más frecuente
        'T': 'o',  # Quinta más frecuente
        'x': 'n',  # Sexta más frecuente
        'g': 'i',  # Séptima más frecuente
        'w': 'r'   # Octava más frecuente
    }
    
    result1 = ''.join([mapping1.get(c, c) for c in message])
    print(f"Mapeo 1: {result1}")
    
    # Buscar patrones de flag
    flag_patterns1 = re.findall(r'[A-Za-z0-9_]{5,}', result1)
    if flag_patterns1:
        print(f"*** Posibles flags en mapeo 1: {flag_patterns1} ***")
    
    # Mapeo 2: Basado en posición alfabética
    mapping2 = {
        'A': 'A', 'D': 'B', 'E': 'C', 'M': 'D',
        'T': 'E', 'g': 'F', 'w': 'G', 'x': 'H'
    }
    
    result2 = ''.join([mapping2.get(c, c) for c in message])
    print(f"Mapeo 2: {result2}")
    
    # Buscar patrones de flag
    flag_patterns2 = re.findall(r'[A-Za-z0-9_]{5,}', result2)
    if flag_patterns2:
        print(f"*** Posibles flags en mapeo 2: {flag_patterns2} ***")
    
    # Mapeo 3: Basado en valores ASCII
    mapping3 = {
        'A': chr(65), 'D': chr(66), 'E': chr(67), 'M': chr(68),
        'T': chr(69), 'g': chr(70), 'w': chr(71), 'x': chr(72)
    }
    
    result3 = ''.join([mapping3.get(c, c) for c in message])
    print(f"Mapeo 3: {result3}")
    
    # Buscar patrones de flag
    flag_patterns3 = re.findall(r'[A-Za-z0-9_]{5,}', result3)
    if flag_patterns3:
        print(f"*** Posibles flags en mapeo 3: {flag_patterns3} ***")
    
    # Mapeo 4: Basado en números
    mapping4 = {
        'A': '1', 'D': '2', 'E': '3', 'M': '4',
        'T': '5', 'g': '6', 'w': '7', 'x': '8'
    }
    
    result4 = ''.join([mapping4.get(c, c) for c in message])
    print(f"Mapeo 4: {result4}")
    
    # Buscar patrones de flag
    flag_patterns4 = re.findall(r'[A-Za-z0-9_]{5,}', result4)
    if flag_patterns4:
        print(f"*** Posibles flags en mapeo 4: {flag_patterns4} ***")
    
    # Mapeo 5: Basado en patrones comunes de flags
    mapping5 = {
        'E': 'H', 'D': 'T', 'M': 'B', 'x': '{',
        'A': 'F', 'T': 'L', 'g': 'A', 'w': 'G'
    }
    
    result5 = ''.join([mapping5.get(c, c) for c in message])
    print(f"Mapeo 5: {result5}")
    
    # Buscar patrones de flag
    flag_patterns5 = re.findall(r'[A-Za-z0-9_]{5,}', result5)
    if flag_patterns5:
        print(f"*** Posibles flags en mapeo 5: {flag_patterns5} ***")
    
    # Mapeo 6: Basado en rotación de caracteres
    mapping6 = {
        'E': 'F', 'D': 'E', 'M': 'N', 'x': 'y',
        'A': 'B', 'T': 'U', 'g': 'h', 'w': 'x'
    }
    
    result6 = ''.join([mapping6.get(c, c) for c in message])
    print(f"Mapeo 6: {result6}")
    
    # Buscar patrones de flag
    flag_patterns6 = re.findall(r'[A-Za-z0-9_]{5,}', result6)
    if flag_patterns6:
        print(f"*** Posibles flags en mapeo 6: {flag_patterns6} ***")
    
    # Mapeo 7: Basado en desplazamiento de 1
    mapping7 = {
        'E': 'F', 'D': 'E', 'M': 'N', 'x': 'y',
        'A': 'B', 'T': 'U', 'g': 'h', 'w': 'x'
    }
    
    result7 = ''.join([mapping7.get(c, c) for c in message])
    print(f"Mapeo 7: {result7}")
    
    # Buscar patrones de flag
    flag_patterns7 = re.findall(r'[A-Za-z0-9_]{5,}', result7)
    if flag_patterns7:
        print(f"*** Posibles flags en mapeo 7: {flag_patterns7} ***")
    
    # Mapeo 8: Basado en desplazamiento de -1
    mapping8 = {
        'E': 'D', 'D': 'C', 'M': 'L', 'x': 'w',
        'A': 'Z', 'T': 'S', 'g': 'f', 'w': 'v'
    }
    
    result8 = ''.join([mapping8.get(c, c) for c in message])
    print(f"Mapeo 8: {result8}")
    
    # Buscar patrones de flag
    flag_patterns8 = re.findall(r'[A-Za-z0-9_]{5,}', result8)
    if flag_patterns8:
        print(f"*** Posibles flags en mapeo 8: {flag_patterns8} ***")
    
    # Mapeo 9: Basado en valores binarios
    mapping9 = {
        'E': '0', 'D': '1', 'M': '0', 'x': '1',
        'A': '0', 'T': '1', 'g': '0', 'w': '1'
    }
    
    result9 = ''.join([mapping9.get(c, c) for c in message])
    print(f"Mapeo 9: {result9}")
    
    # Buscar patrones de flag
    flag_patterns9 = re.findall(r'[A-Za-z0-9_]{5,}', result9)
    if flag_patterns9:
        print(f"*** Posibles flags en mapeo 9: {flag_patterns9} ***")
    
    # Mapeo 10: Basado en valores hexadecimales
    mapping10 = {
        'E': '0', 'D': '1', 'M': '2', 'x': '3',
        'A': '4', 'T': '5', 'g': '6', 'w': '7'
    }
    
    result10 = ''.join([mapping10.get(c, c) for c in message])
    print(f"Mapeo 10: {result10}")
    
    # Buscar patrones de flag
    flag_patterns10 = re.findall(r'[A-Za-z0-9_]{5,}', result10)
    if flag_patterns10:
        print(f"*** Posibles flags en mapeo 10: {flag_patterns10} ***")
    
    # Intentar decodificar como base64 después de la sustitución
    print(f"\n--- Intentando decodificar como base64 después de sustitución ---")
    
    for i, result in enumerate([result1, result2, result3, result4, result5, result6, result7, result8, result9, result10], 1):
        print(f"\nMapeo {i}:")
        print(f"Resultado: {result}")
        
        # Intentar decodificar como base64
        try:
            # Agregar padding si es necesario
            if len(result) % 4 != 0:
                padding_needed = 4 - (len(result) % 4)
                result_padded = result + '=' * padding_needed
            else:
                result_padded = result
            
            decoded = base64.b64decode(result_padded)
            print(f"Decodificado como base64: {decoded}")
            print(f"Como texto: {decoded.decode('utf-8', errors='ignore')}")
            
            # Buscar patrones de flag
            flag_patterns = re.findall(r'[A-Za-z0-9_]{5,}', decoded.decode('utf-8', errors='ignore'))
            if flag_patterns:
                print(f"*** Posibles flags: {flag_patterns} ***")
                
        except Exception as e:
            print(f"Error en decodificación base64: {e}")
    
    return result1, result2, result3, result4, result5

if __name__ == "__main__":
    substitution_cipher()