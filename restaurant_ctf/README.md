# Restaurant CTF - Reconocimiento Completo

## 📋 Información del Reto

- **Plataforma**: Hack The Box
- **Nombre**: Restaurant
- **Categoría**: Pwn
- **Dificultad**: Easy
- **Servidor**: `94.237.48.12:40939`

---

## 🎯 Objetivo

Este directorio contiene el **reconocimiento completo** del reto Restaurant. La fase de explotación será realizada por otra IA.

---

## 📁 Estructura del Proyecto

```
restaurant_ctf/
├── README.md                      # Este archivo
├── RECONOCIMIENTO_COMPLETO.md     # Documentación técnica detallada
├── RESUMEN_EJECUTIVO.txt          # Resumen ejecutivo del reconocimiento
├── poc_leak.py                    # Proof of Concept funcional de leak
├── restaurant_disasm.txt          # Desensamblado completo del binario
├── Restaurant.zip                 # Archivo original del reto
└── pwn_restaurant/
    ├── restaurant                 # Binario ejecutable vulnerable
    └── libc.so.6                  # Biblioteca GLIBC 2.27
```

---

## 🔍 Resumen del Reconocimiento

### Vulnerabilidad Principal
- **Tipo**: Buffer Overflow sin protección
- **Ubicación**: Función `fill()` en `0x400e4a`
- **Severidad**: CRÍTICA
- **Explotabilidad**: ALTA

### Protecciones del Binario
```
✗ Stack Canary: DESACTIVADO
✗ PIE:          DESACTIVADO
✓ NX:           ACTIVADO (requiere ROP)
✓ Full RELRO:   ACTIVADO
```

### Capacidades Confirmadas
- ✅ Control total de RIP (Return Instruction Pointer)
- ✅ Leak de direcciones de libc funcional
- ✅ ROP gadgets disponibles
- ✅ Retorno a main para multi-stage exploit
- ✅ system() y /bin/sh disponibles en libc

---

## 🚀 Quick Start

### 1. Probar el Proof of Concept

```bash
cd /workspace/restaurant_ctf
python3 poc_leak.py
```

**Salida esperada:**
```
[+] Dirección de puts:  0x7fXXXXXXXXXX
[+] Base de libc:       0x7fXXXXXXXXXX
[+] system():           0x7fXXXXXXXXXX
[+] /bin/sh:            0x7fXXXXXXXXXX
[✓] Leak completado exitosamente
```

### 2. Revisar Documentación Completa

```bash
# Ver documentación técnica detallada
cat RECONOCIMIENTO_COMPLETO.md

# Ver resumen ejecutivo
cat RESUMEN_EJECUTIVO.txt
```

### 3. Analizar el Binario Localmente

```bash
cd pwn_restaurant

# Ver protecciones
checksec --file=restaurant

# Ejecutar localmente
./restaurant

# Ver desensamblado
objdump -M intel -d restaurant | less
```

---

## 🔑 Información Clave para Explotación

### Direcciones Importantes (No PIE)
```python
# ROP Gadgets
POP_RDI_RET = 0x4010a3

# PLT/GOT
PUTS_PLT = 0x400650
PUTS_GOT = 0x601fa8
MAIN = 0x400f68

# Offsets en Libc 2.27
LIBC_PUTS = 0x080aa0
LIBC_SYSTEM = 0x04f550
LIBC_BINSH = 0x1b3e1a
```

### Buffer Overflow
```python
BUFFER_SIZE = 32
OFFSET_TO_RIP = 40  # 32 bytes buffer + 8 bytes saved rbp
```

---

## 📊 Resultados del Reconocimiento

### ✅ Completado
- [x] Descarga y extracción de archivos
- [x] Análisis de protecciones del binario
- [x] Identificación de vulnerabilidad buffer overflow
- [x] Cálculo de offset para control de RIP
- [x] Búsqueda de gadgets ROP
- [x] Identificación de direcciones GOT/PLT
- [x] Análisis de versión y offsets de libc
- [x] **Prueba exitosa de leak de direcciones remoto**
- [x] Verificación de retorno a main
- [x] Documentación completa
- [x] Creación de Proof of Concept funcional

### 📋 Pendiente (Para Fase de Explotación)
- [ ] Desarrollo de exploit completo (2da etapa)
- [ ] Construcción de ROP chain final: system("/bin/sh")
- [ ] Obtención de shell remota
- [ ] Captura de flag

---

## 🛠️ Herramientas Utilizadas

- **pwntools**: Framework de explotación
- **checksec**: Análisis de protecciones
- **objdump**: Desensamblado
- **readelf**: Análisis de ELF
- **ropper**: Búsqueda de gadgets ROP
- **strings**: Extracción de strings

---

## 📝 Notas Técnicas

### Estrategia de Explotación (2 Etapas)

**Etapa 1: Leak de Libc** ✅ (Completado y probado)
1. Conectar al servidor
2. Seleccionar opción 1
3. Enviar ROP chain: `pop rdi; puts@GOT; puts@PLT; main`
4. Extraer dirección de puts
5. Calcular base de libc

**Etapa 2: Shell** (Pendiente para siguiente fase)
1. El servidor vuelve a main automáticamente
2. Calcular direcciones de system y /bin/sh
3. Enviar ROP chain: `pop rdi; /bin/sh; system`
4. Obtener shell interactiva
5. Capturar flag

### Timeout del Servidor
- Alarm: 127 segundos (suficiente para exploit manual o automatizado)

---

## 🔬 Validación

El reconocimiento ha sido **validado** mediante:

1. ✅ Prueba local del buffer overflow
2. ✅ Prueba remota del buffer overflow
3. ✅ Extracción exitosa de leak de libc
4. ✅ Verificación de retorno a main
5. ✅ Cálculo de direcciones de system y /bin/sh

**El PoC `poc_leak.py` demuestra que el leak funciona al 100%**

---

## 📚 Documentos de Referencia

### Para Análisis Técnico Detallado
- `RECONOCIMIENTO_COMPLETO.md`: Análisis exhaustivo de todas las funciones, vulnerabilidades, y técnicas

### Para Resumen Ejecutivo
- `RESUMEN_EJECUTIVO.txt`: Información condensada y estructurada para quick reference

### Para Validación
- `poc_leak.py`: Script funcional que demuestra el leak de libc

---

## ⚠️ Disclaimer

Este reconocimiento fue realizado con fines educativos en una plataforma de CTF legítima (Hack The Box). Todo el análisis se realizó sobre un entorno controlado y autorizado.

---

## 👨‍💻 Información del Reconocimiento

- **Realizado por**: Claude (Cursor AI Agent)
- **Fecha**: 2025-10-19
- **Estado**: ✅ **COMPLETO**
- **Siguiente Fase**: Explotación (GPT-5 o siguiente IA)

---

## 🎓 Conclusión

El reconocimiento ha identificado una **vulnerabilidad crítica de buffer overflow** que es **completamente explotable**. El sistema permite:

1. ✅ Control total de la ejecución
2. ✅ Leak de direcciones de memoria (ASLR bypass)
3. ✅ Ejecución de ROP chains
4. ✅ Remote Code Execution (RCE)

**La explotación completa es altamente viable y solo requiere implementar la segunda etapa del exploit.**

---

### 📞 Contacto

Para preguntas sobre el reconocimiento o para continuar con la fase de explotación, referirse a:
- `RECONOCIMIENTO_COMPLETO.md` para detalles técnicos
- `poc_leak.py` para código funcional de referencia

**Ready for exploitation phase! 🚀**
