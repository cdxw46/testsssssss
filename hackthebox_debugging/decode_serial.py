#!/usr/bin/env python3

import struct
import sys
import signal
import time

def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

# Set timeout for the entire script
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(15)  # 15 second timeout

def parse_saleae_file(filename):
    """Parse Saleae Logic Analyzer file and extract digital data"""
    with open(filename, 'rb') as f:
        # Read header
        header = f.read(8)
        if header != b'<SALEAE>':
            print("Not a valid Saleae file")
            return None
        
        # Read version and other metadata
        version = struct.unpack('<I', f.read(4))[0]
        print(f"Saleae file version: {version}")
        
        # Read more metadata
        data_size = struct.unpack('<I', f.read(4))[0]
        print(f"Data size: {data_size}")
        
        # Read sample rate and other info
        sample_rate = struct.unpack('<d', f.read(8))[0]
        print(f"Sample rate: {sample_rate} Hz")
        
        # Read more metadata
        f.read(8)  # Skip some bytes
        
        # Read the actual digital data
        digital_data = f.read()
        
        return digital_data, sample_rate

def decode_uart_data(digital_data, sample_rate, baud_rate=115200):
    """Decode UART data from digital signal"""
    # Calculate samples per bit
    samples_per_bit = int(sample_rate / baud_rate)
    print(f"Samples per bit: {samples_per_bit}")
    
    # Convert digital data to binary string
    binary_data = []
    for byte in digital_data:
        for i in range(8):
            bit = (byte >> i) & 1
            binary_data.append(bit)
    
    print(f"Total bits: {len(binary_data)}")
    
    # Look for start bits (0) and decode UART frames
    decoded_bytes = []
    i = 0
    
    while i < len(binary_data) - 10 * samples_per_bit:
        # Look for start bit (0)
        if binary_data[i] == 0:
            # Found potential start bit, decode the frame
            byte_value = 0
            bit_pos = 0
            
            # Skip start bit
            i += samples_per_bit
            
            # Read 8 data bits (LSB first)
            for bit_idx in range(8):
                if i + samples_per_bit//2 < len(binary_data):
                    bit_value = binary_data[i + samples_per_bit//2]
                    byte_value |= (bit_value << bit_pos)
                    bit_pos += 1
                    i += samples_per_bit
                else:
                    break
            
            # Skip stop bit
            i += samples_per_bit
            
            if byte_value != 0:  # Skip null bytes
                decoded_bytes.append(byte_value)
                print(f"Decoded byte: 0x{byte_value:02x} ('{chr(byte_value) if 32 <= byte_value <= 126 else '.'}')")
        else:
            i += 1
    
    return decoded_bytes

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 decode_serial.py <digital_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Parse the Saleae file
    result = parse_saleae_file(filename)
    if result is None:
        sys.exit(1)
    
    digital_data, sample_rate = result
    
    # Try different baud rates
    baud_rates = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]
    
    for baud_rate in baud_rates:
        print(f"\n=== Trying baud rate: {baud_rate} ===")
        decoded_bytes = decode_uart_data(digital_data, sample_rate, baud_rate)
        
        if decoded_bytes:
            print(f"Decoded {len(decoded_bytes)} bytes at {baud_rate} baud:")
            try:
                decoded_text = ''.join(chr(b) for b in decoded_bytes if 32 <= b <= 126)
                print(f"Text: {decoded_text}")
                
                # Look for flag pattern
                if 'HTB{' in decoded_text or 'flag' in decoded_text.lower():
                    print(f"*** POTENTIAL FLAG FOUND: {decoded_text} ***")
            except:
                pass

if __name__ == "__main__":
    main()