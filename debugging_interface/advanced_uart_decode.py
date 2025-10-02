#!/usr/bin/env python3

import struct
import sys

def parse_saleae_binary(filename):
    """
    Parsea archivo binario de Saleae y extrae datos de señal
    """
    print(f"Analizando archivo: {filename}")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    if not data.startswith(b'<SALEAE>'):
        print("Error: No es un archivo Saleae válido")
        return None, None
    
    # Buscar metadatos
    header_pos = data.find(b'<SALEAE>')
    if header_pos == -1:
        return None, None
    
    # Saltar header y buscar datos
    pos = header_pos + 8
    
    # Leer versión (4 bytes)
    version = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    print(f"Versión: {version}")
    
    # Leer tamaño de datos (4 bytes)
    data_size = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    print(f"Tamaño de datos: {data_size}")
    
    # Leer configuración (4 bytes)
    config = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    
    # Buscar datos reales - buscar patrones de timestamps
    # Los datos están en formato: timestamp (8 bytes) + valor (1 byte)
    
    samples = []
    while pos < len(data) - 12:
        try:
            # Leer timestamp (8 bytes, little-endian)
            timestamp = struct.unpack('<Q', data[pos:pos+8])[0]
            pos += 8
            
            # Leer valor de señal (1 byte)
            value = data[pos]
            pos += 1
            
            samples.append((timestamp, value))
            
        except struct.error:
            break
    
    print(f"Total de muestras: {len(samples)}")
    if samples:
        print(f"Primera muestra: timestamp={samples[0][0]}, valor={samples[0][1]}")
        print(f"Última muestra: timestamp={samples[-1][0]}, valor={samples[-1][1]}")
    
    return samples, 50000000  # Frecuencia de muestreo de los metadatos

def decode_uart_from_samples(samples, sample_rate, baud_rate=9600):
    """
    Decodifica UART desde muestras de señal digital
    """
    if not samples:
        return ""
    
    print(f"Decodificando UART: {baud_rate} baud, {sample_rate} Hz muestreo")
    
    # Calcular duración de bit en muestras
    bit_duration = sample_rate // baud_rate
    print(f"Duración de bit: {bit_duration} muestras")
    
    # Encontrar transiciones de señal (cambios de 0 a 1 o 1 a 0)
    transitions = []
    for i in range(1, len(samples)):
        if samples[i-1][1] != samples[i][1]:
            transitions.append(samples[i])
    
    print(f"Transiciones encontradas: {len(transitions)}")
    
    # Buscar start bits (transición de 1 a 0)
    start_bits = []
    for i in range(1, len(transitions)):
        if transitions[i-1][1] == 1 and transitions[i][1] == 0:
            start_bits.append(transitions[i])
    
    print(f"Start bits encontrados: {len(start_bits)}")
    
    # Decodificar caracteres desde start bits
    decoded_chars = []
    
    for start_bit in start_bits:
        start_time = start_bit[0]
        
        # Buscar los próximos 8 bits de datos
        char_bits = []
        current_time = start_time
        
        for bit_num in range(8):
            # Calcular tiempo para este bit (1.5, 2.5, 3.5, ... veces la duración del bit)
            bit_time = start_time + int((1.5 + bit_num) * bit_duration)
            
            # Encontrar el valor de la señal en ese momento
            bit_value = 0
            for sample in samples:
                if sample[0] >= bit_time:
                    bit_value = sample[1]
                    break
            
            char_bits.append(bit_value)
        
        # Convertir bits a carácter
        char_value = 0
        for i, bit in enumerate(char_bits):
            char_value |= (bit << i)
        
        if 32 <= char_value <= 126:  # Caracteres imprimibles
            decoded_chars.append(chr(char_value))
    
    return ''.join(decoded_chars)

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 advanced_uart_decode.py <archivo.bin>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Parsear archivo
    samples, sample_rate = parse_saleae_binary(filename)
    
    if samples is None:
        print("Error al parsear archivo")
        sys.exit(1)
    
    # Intentar diferentes velocidades de baud
    baud_rates = [9600, 115200, 57600, 38400, 19200, 4800, 2400, 1200]
    
    for baud_rate in baud_rates:
        print(f"\n=== Probando {baud_rate} baud ===")
        decoded = decode_uart_from_samples(samples, sample_rate, baud_rate)
        if decoded:
            print(f"Texto decodificado: {repr(decoded)}")
            if any(c.isprintable() and c not in '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x7f' for c in decoded):
                print(f"*** POSIBLE FLAG: {decoded} ***")

if __name__ == "__main__":
    main()