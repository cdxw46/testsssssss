#!/usr/bin/env python3

import struct
import sys

def parse_saleae_correct(filename):
    """Parse Saleae file with correct format understanding"""
    print(f"Parsing {filename} with correct format")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Skip header and extract samples
    header_pos = data.find(b'<SALEAE>')
    if header_pos == -1:
        return None
    
    pos = header_pos + 8
    version = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    data_size = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    config = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    
    print(f"Version: {version}, Data size: {data_size}")
    
    # Extract samples - the format might be different
    samples = []
    
    # Try different parsing approaches
    # Method 1: Standard Saleae format
    while pos < len(data) - 8:
        try:
            timestamp = struct.unpack('<Q', data[pos:pos+8])[0]
            pos += 8
            value = data[pos]
            pos += 1
            samples.append((timestamp, value))
            
            # Skip padding
            while pos < len(data) and data[pos] == 0:
                pos += 1
        except:
            break
    
    print(f"Extracted {len(samples)} samples")
    return samples

def decode_uart_31230(samples):
    """Decode UART with correct baud rate of 31230"""
    print("Decoding UART with 31230 baud rate")
    
    if not samples:
        return None
    
    sample_rate = 50000000  # 50MHz
    baud_rate = 31230
    bit_duration = sample_rate // baud_rate
    
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Baud rate: {baud_rate} bps")
    print(f"Bit duration: {bit_duration} samples")
    
    # Find transitions
    transitions = []
    for i in range(1, len(samples)):
        if samples[i-1][1] != samples[i][1]:
            transitions.append((i, samples[i][0], samples[i][1]))
    
    print(f"Found {len(transitions)} transitions")
    
    # Decode UART
    decoded_chars = []
    
    for i in range(len(transitions) - 10):
        # Look for start bit (high to low)
        if transitions[i][2] == 0 and i > 0 and transitions[i-1][2] == 1:
            start_sample = transitions[i][0]
            
            # Decode 8 data bits
            char_bits = []
            for bit_num in range(8):
                bit_sample = start_sample + int((1.5 + bit_num) * bit_duration)
                
                if bit_sample < len(samples):
                    char_bits.append(samples[bit_sample][1])
            
            # Convert to character
            if len(char_bits) == 8:
                char_value = 0
                for j, bit in enumerate(char_bits):
                    char_value |= (bit << j)
                
                if 32 <= char_value <= 126:
                    decoded_chars.append(chr(char_value))
                    print(f"Decoded: '{chr(char_value)}'")
    
    return ''.join(decoded_chars)

def alternative_decode_31230(filename):
    """Alternative method to decode with 31230 baud"""
    print("Trying alternative decode method")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Skip header
    header_pos = data.find(b'<SALEAE>')
    if header_pos == -1:
        return None
    
    # Look for signal data after header
    signal_data = data[header_pos + 8:]
    
    # Try to interpret as raw signal data
    # Look for patterns that might be UART frames
    
    # Convert bytes to signal levels (0 or 1)
    signal_bits = []
    for byte in signal_data:
        if byte in [0x00, 0x01]:
            signal_bits.append(byte)
        else:
            # Try to extract bits from other values
            for i in range(8):
                signal_bits.append((byte >> i) & 1)
    
    print(f"Extracted {len(signal_bits)} signal bits")
    
    # Decode UART with 31230 baud
    sample_rate = 50000000
    baud_rate = 31230
    samples_per_bit = sample_rate // baud_rate
    
    print(f"Samples per bit: {samples_per_bit}")
    
    # Look for start bits and decode characters
    chars = []
    i = 0
    while i < len(signal_bits) - samples_per_bit * 10:
        if signal_bits[i] == 0:  # Start bit
            # Read 8 data bits
            data_bits = []
            for j in range(8):
                bit_pos = i + (j + 1) * samples_per_bit
                if bit_pos < len(signal_bits):
                    data_bits.append(signal_bits[bit_pos])
            
            if len(data_bits) == 8:
                char_value = 0
                for k, bit in enumerate(data_bits):
                    char_value |= (bit << k)
                
                if 32 <= char_value <= 126:
                    chars.append(chr(char_value))
                    print(f"Decoded char: '{chr(char_value)}'")
            
            i += samples_per_bit * 10  # Skip entire frame
        else:
            i += 1
    
    return ''.join(chars)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 correct_uart_decoder.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    print("=== METHOD 1: Standard Saleae parsing ===")
    samples = parse_saleae_correct(filename)
    if samples:
        result = decode_uart_31230(samples)
        if result:
            print(f"Result: {result}")
            if 'HTB{' in result:
                print(f"*** FLAG FOUND: {result} ***")
                return
    
    print("\n=== METHOD 2: Alternative parsing ===")
    result = alternative_decode_31230(filename)
    if result:
        print(f"Alternative result: {result}")
        if 'HTB{' in result:
            print(f"*** FLAG FOUND: {result} ***")
            return
    
    print("\nNo flag found with 31230 baud rate")

if __name__ == "__main__":
    main()