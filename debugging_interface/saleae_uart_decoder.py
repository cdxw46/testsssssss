#!/usr/bin/env python3

import struct
import sys
import json

def parse_saleae_metadata(meta_file):
    """Parse Saleae metadata JSON file"""
    with open(meta_file, 'r') as f:
        metadata = json.load(f)
    
    # Extract sample rate from metadata - search for sampleRate in the JSON
    sample_rate = None
    def find_sample_rate(obj):
        if isinstance(obj, dict):
            if 'sampleRate' in obj and isinstance(obj['sampleRate'], dict):
                if 'digital' in obj['sampleRate']:
                    return obj['sampleRate']['digital']
            for value in obj.values():
                result = find_sample_rate(value)
                if result:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = find_sample_rate(item)
                if result:
                    return result
        return None
    
    sample_rate = find_sample_rate(metadata)
    if sample_rate:
        print(f"Sample rate from metadata: {sample_rate} Hz")
    else:
        print("Could not find sample rate in metadata")
        sample_rate = 50000000  # Default fallback
    
    return sample_rate

def parse_saleae_binary_v2(filename, sample_rate):
    """
    Parse Saleae binary file with improved algorithm
    """
    print(f"Parsing {filename} with sample rate {sample_rate}")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
    # Saleae format: header + data blocks
    # Each data block: timestamp (8 bytes) + value (1 byte)
    
    samples = []
    pos = 0
    
    # Skip header
    while pos < len(data) - 12:
        if data[pos:pos+8] == b'<SALEAE>':
            pos += 8
            break
        pos += 1
    
    if pos >= len(data) - 12:
        print("Could not find Saleae header")
        return None
    
    print(f"Found header at position {pos}")
    
    # Read data blocks
    while pos < len(data) - 12:
        try:
            # Read timestamp (8 bytes, little-endian)
            timestamp = struct.unpack('<Q', data[pos:pos+8])[0]
            pos += 8
            
            # Read value (1 byte)
            value = data[pos]
            pos += 1
            
            # Skip padding if any
            while pos < len(data) and data[pos] == 0:
                pos += 1
            
            samples.append((timestamp, value))
            
        except struct.error:
            break
    
    print(f"Total samples: {len(samples)}")
    
    if samples:
        print(f"First sample: timestamp={samples[0][0]}, value={samples[0][1]}")
        print(f"Last sample: timestamp={samples[-1][0]}, value={samples[-1][1]}")
        
        # Find signal transitions
        transitions = []
        for i in range(1, len(samples)):
            if samples[i-1][1] != samples[i][1]:
                transitions.append((i, samples[i]))
        
        print(f"Signal transitions: {len(transitions)}")
        
        # Look for UART patterns
        # UART: start bit (0) + 8 data bits + stop bit (1)
        uart_chars = []
        
        for i in range(len(transitions) - 10):
            # Check if this could be a start bit (1->0 transition)
            if transitions[i][1][1] == 0 and i > 0 and transitions[i-1][1][1] == 1:
                # Found potential start bit
                start_time = transitions[i][1][0]
                
                # Try to decode 8 data bits
                char_bits = []
                bit_times = []
                
                for bit_num in range(8):
                    # Calculate expected bit time (1.5, 2.5, 3.5, ... bit periods)
                    expected_time = start_time + (1.5 + bit_num) * (sample_rate // 9600)  # Assume 9600 baud
                    bit_times.append(expected_time)
                    
                    # Find closest sample to this time
                    closest_sample = None
                    min_diff = float('inf')
                    
                    for sample in samples:
                        diff = abs(sample[0] - expected_time)
                        if diff < min_diff:
                            min_diff = diff
                            closest_sample = sample
                    
                    if closest_sample:
                        char_bits.append(closest_sample[1])
                
                # Convert bits to character
                if len(char_bits) == 8:
                    char_value = 0
                    for j, bit in enumerate(char_bits):
                        char_value |= (bit << j)
                    
                    # Check if it's a printable character
                    if 32 <= char_value <= 126:
                        uart_chars.append(chr(char_value))
                        print(f"Found character: '{chr(char_value)}' (0x{char_value:02x}) at time {start_time}")
        
        return ''.join(uart_chars)
    
    return None

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 saleae_uart_decoder.py <binary_file> <metadata_file>")
        sys.exit(1)
    
    binary_file = sys.argv[1]
    metadata_file = sys.argv[2]
    
    # Parse metadata to get sample rate
    sample_rate = parse_saleae_metadata(metadata_file)
    
    # Parse binary file
    decoded_text = parse_saleae_binary_v2(binary_file, sample_rate)
    
    if decoded_text:
        print(f"\nDecoded text: {repr(decoded_text)}")
        
        # Look for flag pattern
        if 'HTB{' in decoded_text or 'flag' in decoded_text.lower():
            print(f"\n*** POTENTIAL FLAG FOUND: {decoded_text} ***")
    else:
        print("No text decoded")

if __name__ == "__main__":
    main()