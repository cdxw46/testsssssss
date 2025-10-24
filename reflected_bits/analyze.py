#!/usr/bin/env python3

import base64
import re

def analyze_message():
    message = "=EDMxETMxEDMgATMxEDMwEDMgEDMxATMwEDMgATMxADMwEDMgETMxETMwEDMgEDMwETMwEDMgATMwATMwEDMgEDMwADMwEDMgATMxEDMwEDMgEDMwEDMwEDMgATMwADMwEDMgETMxETMwEDMgADMxADMwEDMgATMxEDMwEDMgEDMwADMwEDMgETMxETMwEDMgEDMxADMwEDMgETMwATMwEDMgATMwATMwEDMgADMwATMxADMgEDMxEDMwEDMgETMwETMxEDMgEDMxADMwEDMgADMxATMwEDMgETMxADMwEDMgATMxADMwEDM"
    
    print("Mensaje original:")
    print(message)
    print("\n" + "="*50)
    
    # Remover el = del inicio
    if message.startswith('='):
        message = message[1:]
    
    print("Mensaje sin = inicial:")
    print(message)
    print("\n" + "="*50)
    
    # Analizar el patrón de 4 caracteres
    pattern = re.findall(r'.{4}', message)
    print("Patrones de 4 caracteres encontrados:")
    for i, p in enumerate(pattern):
        print(f"{i:2d}: {p}")
    
    print("\n" + "="*50)
    
    # Intentar decodificar como base64
    try:
        decoded = base64.b64decode(message)
        print("Decodificación base64:")
        print(decoded)
        print("Como string:")
        print(decoded.decode('utf-8', errors='ignore'))
    except Exception as e:
        print(f"Error en decodificación base64: {e}")
    
    print("\n" + "="*50)
    
    # Analizar los caracteres únicos
    unique_chars = set(message)
    print("Caracteres únicos en el mensaje:")
    print(sorted(unique_chars))
    
    # Ver si hay un patrón en los últimos caracteres
    print("\nÚltimos caracteres del mensaje:")
    print(message[-10:])
    
    # Verificar si el mensaje es múltiplo de 4
    print(f"\nLongitud del mensaje: {len(message)}")
    print(f"¿Es múltiplo de 4? {len(message) % 4 == 0}")
    
    # Si no es múltiplo de 4, agregar padding
    if len(message) % 4 != 0:
        padding_needed = 4 - (len(message) % 4)
        message_padded = message + '=' * padding_needed
        print(f"Mensaje con padding: {message_padded}")
        
        try:
            decoded_padded = base64.b64decode(message_padded)
            print("Decodificación base64 con padding:")
            print(decoded_padded)
            print("Como string:")
            print(decoded_padded.decode('utf-8', errors='ignore'))
        except Exception as e:
            print(f"Error en decodificación base64 con padding: {e}")

if __name__ == "__main__":
    analyze_message()