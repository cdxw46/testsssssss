#!/usr/bin/env python3

import struct
import sys
import json

def parse_saleae_samples(filename):
    """Parse Saleae binary file to extract signal samples"""
    print(f"Parsing Saleae file: {filename}")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Find and skip header
    header_pos = data.find(b'<SALEAE>')
    if header_pos == -1:
        print("No Saleae header found")
        return None
    
    # Parse header
    pos = header_pos + 8
    version = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    data_size = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    config = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    
    print(f"Version: {version}, Data size: {data_size}, Config: {config}")
    
    # Extract samples
    samples = []
    while pos < len(data) - 8:
        try:
            # Read timestamp (8 bytes, little-endian)
            timestamp = struct.unpack('<Q', data[pos:pos+8])[0]
            pos += 8
            
            # Read value (1 byte)
            value = data[pos]
            pos += 1
            
            samples.append((timestamp, value))
            
            # Skip padding
            while pos < len(data) and data[pos] == 0:
                pos += 1
                
        except struct.error:
            break
    
    print(f"Extracted {len(samples)} samples")
    return samples

def decode_uart_timing(samples, sample_rate, baud_rate):
    """Decode UART using timing analysis"""
    print(f"Decoding UART: {baud_rate} baud, {sample_rate} Hz sample rate")
    
    if not samples:
        return None
    
    # Calculate bit duration in samples
    bit_duration = sample_rate // baud_rate
    print(f"Bit duration: {bit_duration} samples")
    
    # Find signal transitions
    transitions = []
    for i in range(1, len(samples)):
        if samples[i-1][1] != samples[i][1]:
            transitions.append((i, samples[i][0], samples[i][1]))
    
    print(f"Found {len(transitions)} signal transitions")
    
    # Look for UART start bits (high to low transition)
    decoded_chars = []
    
    for i in range(len(transitions) - 10):
        # Check for start bit (high to low)
        if transitions[i][2] == 0 and i > 0 and transitions[i-1][2] == 1:
            start_time = transitions[i][1]
            start_sample = transitions[i][0]
            
            # Try to decode 8 data bits
            char_bits = []
            
            for bit_num in range(8):
                # Calculate sample index for this bit (1.5, 2.5, 3.5, ... bit periods)
                bit_sample = start_sample + int((1.5 + bit_num) * bit_duration)
                
                if bit_sample < len(samples):
                    char_bits.append(samples[bit_sample][1])
            
            # Convert bits to character (LSB first for UART)
            if len(char_bits) == 8:
                char_value = 0
                for j, bit in enumerate(char_bits):
                    char_value |= (bit << j)
                
                if 32 <= char_value <= 126:  # Printable ASCII
                    decoded_chars.append(chr(char_value))
                    print(f"Decoded char: '{chr(char_value)}' (0x{char_value:02x}) at time {start_time}")
    
    return ''.join(decoded_chars)

def alternative_timing_decode(samples):
    """Alternative decoding method using time differences"""
    print("Trying alternative timing decode...")
    
    if not samples:
        return None
    
    # Calculate time differences between transitions
    transitions = []
    for i in range(1, len(samples)):
        if samples[i-1][1] != samples[i][1]:
            time_diff = samples[i][0] - samples[i-1][0]
            transitions.append((samples[i][0], samples[i][1], time_diff))
    
    print(f"Found {len(transitions)} transitions with timing")
    
    # Look for patterns that might indicate UART communication
    # UART typically has: start bit (long), data bits (short), stop bit (long)
    
    decoded_chars = []
    
    for i in range(len(transitions) - 10):
        # Look for start bit pattern
        if transitions[i][1] == 0:  # Low signal
            # Check if previous was high
            if i > 0 and transitions[i-1][1] == 1:
                # This could be a start bit
                start_time = transitions[i][0]
                
                # Look for 8 data bits followed by stop bit
                data_bits = []
                current_time = start_time
                
                for bit_num in range(8):
                    # Find next transition
                    next_transition = None
                    for j in range(i+1, min(i+20, len(transitions))):
                        if transitions[j][0] > current_time + (bit_num + 1) * 1000:  # Rough timing
                            next_transition = transitions[j]
                            break
                    
                    if next_transition:
                        data_bits.append(next_transition[1])
                        current_time = next_transition[0]
                    else:
                        break
                
                # Convert to character
                if len(data_bits) == 8:
                    char_value = 0
                    for j, bit in enumerate(data_bits):
                        char_value |= (bit << j)
                    
                    if 32 <= char_value <= 126:
                        decoded_chars.append(chr(char_value))
    
    return ''.join(decoded_chars)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 real_uart_decoder.py <binary_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Parse samples from Saleae file
    samples = parse_saleae_samples(filename)
    
    if not samples:
        print("Failed to parse samples")
        sys.exit(1)
    
    # Try different baud rates
    sample_rate = 50000000  # 50MHz from metadata
    
    baud_rates = [9600, 115200, 57600, 38400, 19200, 4800, 2400, 1200]
    
    print("\n=== TIMING-BASED UART DECODING ===")
    for baud_rate in baud_rates:
        print(f"\nTrying {baud_rate} baud:")
        decoded = decode_uart_timing(samples, sample_rate, baud_rate)
        if decoded:
            print(f"Result: {repr(decoded)}")
            if 'HTB{' in decoded or 'flag' in decoded.lower():
                print(f"*** POTENTIAL FLAG: {decoded} ***")
                return
    
    print("\n=== ALTERNATIVE TIMING DECODE ===")
    decoded = alternative_timing_decode(samples)
    if decoded:
        print(f"Alternative result: {repr(decoded)}")
        if 'HTB{' in decoded or 'flag' in decoded.lower():
            print(f"*** POTENTIAL FLAG: {decoded} ***")
    
    # If no clear result, show sample statistics
    print(f"\n=== SAMPLE STATISTICS ===")
    print(f"Total samples: {len(samples)}")
    if samples:
        print(f"First sample: timestamp={samples[0][0]}, value={samples[0][1]}")
        print(f"Last sample: timestamp={samples[-1][0]}, value={samples[-1][1]}")
        
        # Count signal levels
        high_count = sum(1 for _, val in samples if val == 1)
        low_count = sum(1 for _, val in samples if val == 0)
        print(f"High signals: {high_count}, Low signals: {low_count}")

if __name__ == "__main__":
    main()