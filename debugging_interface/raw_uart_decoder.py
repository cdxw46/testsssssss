#!/usr/bin/env python3

import struct
import sys

def decode_uart_raw(filename):
    """Decode UART from raw binary data"""
    print(f"Decoding UART from {filename}")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
    # Skip Saleae header
    header_pos = data.find(b'<SALEAE>')
    if header_pos == -1:
        print("No Saleae header found")
        return
    
    print(f"Header found at position {header_pos}")
    
    # Start after header
    pos = header_pos + 8
    
    # Try to extract signal data
    # Look for patterns that might be signal transitions
    
    # Method 1: Look for alternating 0/1 patterns
    print("\nMethod 1: Looking for alternating signal patterns")
    
    # Find all non-zero bytes that might represent signal levels
    signal_bytes = []
    for i in range(pos, len(data)):
        byte_val = data[i]
        if byte_val in [0x00, 0x01]:
            signal_bytes.append(byte_val)
    
    print(f"Found {len(signal_bytes)} potential signal bytes")
    
    if signal_bytes:
        # Look for UART start bit patterns (transition from 1 to 0)
        uart_data = []
        
        for i in range(len(signal_bytes) - 10):
            if signal_bytes[i] == 1 and signal_bytes[i+1] == 0:
                # Potential start bit found
                # Try to read 8 data bits
                data_bits = []
                for j in range(8):
                    if i + 2 + j < len(signal_bytes):
                        data_bits.append(signal_bytes[i + 2 + j])
                
                if len(data_bits) == 8:
                    # Convert bits to character (LSB first)
                    char_value = 0
                    for k, bit in enumerate(data_bits):
                        char_value |= (bit << k)
                    
                    if 32 <= char_value <= 126:  # Printable ASCII
                        uart_data.append(chr(char_value))
        
        if uart_data:
            result = ''.join(uart_data)
            print(f"UART data (Method 1): {repr(result)}")
            return result
    
    # Method 2: Interpret raw bytes as UART data
    print("\nMethod 2: Interpreting raw bytes as UART")
    
    # Look for patterns in the raw data
    # Try different byte offsets and interpretations
    
    for offset in [0, 1, 2, 4, 8]:
        print(f"\nTrying offset {offset}:")
        chunk = data[header_pos + offset:]
        
        # Look for sequences that might be ASCII characters
        ascii_chars = []
        for i in range(0, len(chunk) - 7, 8):
            # Try to interpret 8 bytes as a character
            byte_sequence = chunk[i:i+8]
            
            # Method 2a: Direct byte interpretation
            if len(byte_sequence) >= 8:
                # Check if this looks like a UART frame
                if byte_sequence[0] == 0:  # Start bit
                    char_value = 0
                    for j in range(8):
                        char_value |= (byte_sequence[j+1] << j)
                    
                    if 32 <= char_value <= 126:
                        ascii_chars.append(chr(char_value))
        
        if ascii_chars:
            result = ''.join(ascii_chars)
            print(f"ASCII chars at offset {offset}: {repr(result)}")
            if 'HTB{' in result or 'flag' in result.lower():
                print(f"*** POTENTIAL FLAG: {result} ***")
                return result
    
    # Method 3: Look for embedded text in the binary
    print("\nMethod 3: Looking for embedded text")
    
    # Search for common text patterns
    text_patterns = [
        b'debugging',
        b'interface',
        b'serial',
        b'uart',
        b'flag',
        b'HTB',
        b'hackthebox'
    ]
    
    for pattern in text_patterns:
        pos = data.find(pattern)
        if pos != -1:
            print(f"Found '{pattern.decode()}' at position {pos}")
            # Extract surrounding context
            start = max(0, pos - 20)
            end = min(len(data), pos + 50)
            context = data[start:end]
            print(f"Context: {context}")
    
    return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 raw_uart_decoder.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    result = decode_uart_raw(filename)
    
    if result:
        print(f"\nFinal result: {result}")
    else:
        print("\nNo UART data decoded")

if __name__ == "__main__":
    main()