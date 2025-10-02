#!/usr/bin/env python3

import struct
import sys

def analyze_binary_structure(filename):
    """
    Analiza la estructura del archivo binario en detalle
    """
    print(f"Analizando estructura de: {filename}")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"Tamaño total: {len(data)} bytes")
    
    # Mostrar primeros 200 bytes en hex
    print("\nPrimeros 200 bytes (hex):")
    for i in range(0, min(200, len(data)), 16):
        hex_part = ' '.join(f'{b:02x}' for b in data[i:i+16])
        ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data[i:i+16])
        print(f"{i:08x}: {hex_part:<48} |{ascii_part}|")
    
    # Buscar patrones repetitivos
    print("\nBuscando patrones de 8 bytes (posibles timestamps):")
    for i in range(0, min(500, len(data)-8), 8):
        chunk = data[i:i+8]
        if len(chunk) == 8:
            # Intentar interpretar como timestamp
            timestamp = struct.unpack('<Q', chunk)[0]
            if timestamp > 0 and timestamp < 10000000000000000000:  # Rango razonable
                print(f"Posición {i:08x}: {timestamp} (0x{timestamp:016x})")
    
    # Buscar valores que podrían ser datos de señal (0 o 1)
    print("\nBuscando valores de señal (0x00, 0x01):")
    signal_positions = []
    for i, byte in enumerate(data):
        if byte == 0x00 or byte == 0x01:
            signal_positions.append((i, byte))
            if len(signal_positions) > 20:  # Limitar output
                break
    
    for pos, val in signal_positions:
        print(f"Posición {pos:08x}: valor {val}")
    
    # Buscar secuencias que podrían ser texto
    print("\nBuscando secuencias de texto ASCII:")
    text_candidates = []
    for i in range(len(data) - 4):
        chunk = data[i:i+4]
        try:
            text = chunk.decode('ascii')
            if text.isprintable() and any(c.isalpha() for c in text):
                text_candidates.append((i, text))
        except:
            pass
    
    for pos, text in text_candidates[:10]:  # Mostrar solo los primeros 10
        print(f"Posición {pos:08x}: '{text}'")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 analyze_binary.py <archivo.bin>")
        sys.exit(1)
    
    filename = sys.argv[1]
    analyze_binary_structure(filename)

if __name__ == "__main__":
    main()