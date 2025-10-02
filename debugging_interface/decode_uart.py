#!/usr/bin/env python3

import struct
import sys

def decode_saleae_uart(filename, baud_rate=9600, data_bits=8, stop_bits=1, parity='none'):
    """
    Decodifica archivo Saleae como UART
    """
    print(f"Decodificando {filename} como UART ({baud_rate} baud, {data_bits} bits)")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Verificar header Saleae
    if not data.startswith(b'<SALEAE>'):
        print("Error: No es un archivo Saleae válido")
        return
    
    print(f"Tamaño del archivo: {len(data)} bytes")
    
    # Buscar datos después del header
    header_end = data.find(b'\x01\x00\x00\x00')
    if header_end == -1:
        print("Error: No se encontró fin de header")
        return
    
    # Extraer metadatos
    header_end += 4
    sample_rate = struct.unpack('<I', data[header_end:header_end+4])[0]
    print(f"Frecuencia de muestreo: {sample_rate} Hz")
    
    # Calcular bits por muestra
    bit_duration = sample_rate // baud_rate
    print(f"Duración de bit: {bit_duration} muestras")
    
    # Buscar datos de señal
    # Los datos están en formato de timestamps + valores
    # Buscar patrones de transición que indiquen start bit
    decoded_chars = []
    
    # Buscar secuencias que parezcan caracteres ASCII
    # Un carácter típico: start bit (0) + 8 data bits + stop bit (1)
    
    # Método simple: buscar patrones en los datos
    print("\nBuscando patrones de datos...")
    
    # Convertir a string para buscar patrones
    try:
        # Buscar secuencias que puedan ser texto
        for i in range(0, len(data)-8, 8):
            chunk = data[i:i+8]
            try:
                # Intentar interpretar como caracteres
                text = chunk.decode('ascii', errors='ignore')
                if text.isprintable() and len(text.strip()) > 0:
                    print(f"Posición {i}: {repr(text)}")
            except:
                pass
    except Exception as e:
        print(f"Error en decodificación: {e}")
    
    return decoded_chars

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 decode_uart.py <archivo.bin>")
        sys.exit(1)
    
    filename = sys.argv[1]
    decode_saleae_uart(filename)

if __name__ == "__main__":
    main()