#!/usr/bin/env python3

import struct
import sys
import re
import json

def extract_all_text_methods(filename):
    """Try all possible methods to extract text from the file"""
    print(f"=== FINAL DECODER FOR {filename} ===")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
    results = []
    
    # Method 1: Direct ASCII search
    print("\n--- Method 1: Direct ASCII Search ---")
    ascii_text = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data)
    print(f"ASCII representation: {ascii_text[:200]}...")
    
    # Look for flag patterns
    flag_matches = re.findall(r'[A-Za-z0-9_{}]{10,}', ascii_text)
    for match in flag_matches:
        if any(keyword in match.lower() for keyword in ['htb', 'flag', 'debug', 'interface']):
            print(f"Potential flag pattern: {match}")
            results.append(match)
    
    # Method 2: XOR with common keys
    print("\n--- Method 2: XOR Decoding ---")
    for xor_key in [0x42, 0x55, 0xAA, 0xFF, 0x01, 0x80]:
        xor_data = bytes(b ^ xor_key for b in data)
        xor_text = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in xor_data)
        if any(keyword in xor_text.lower() for keyword in ['htb', 'flag', 'debug']):
            print(f"XOR with 0x{xor_key:02X} found: {xor_text[:100]}")
            results.append(xor_text)
    
    # Method 3: Bit manipulation
    print("\n--- Method 3: Bit Manipulation ---")
    # Try interpreting as UART with different bit orders
    for bit_order in ['lsb', 'msb']:
        for baud in [9600, 115200, 57600, 38400, 19200]:
            decoded = decode_uart_bits(data, baud, bit_order)
            if decoded and len(decoded.strip()) > 0:
                print(f"UART {bit_order} {baud} baud: {repr(decoded[:50])}")
                if any(keyword in decoded.lower() for keyword in ['htb', 'flag', 'debug']):
                    results.append(decoded)
    
    # Method 4: Base64 and other encodings
    print("\n--- Method 4: Encoding Detection ---")
    try:
        import base64
        # Try base64 decoding
        try:
            b64_decoded = base64.b64decode(data)
            b64_text = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in b64_decoded)
            if any(keyword in b64_text.lower() for keyword in ['htb', 'flag', 'debug']):
                print(f"Base64 decoded: {b64_text}")
                results.append(b64_text)
        except:
            pass
    except ImportError:
        pass
    
    # Method 5: Frequency analysis
    print("\n--- Method 5: Frequency Analysis ---")
    byte_freq = {}
    for byte in data:
        byte_freq[byte] = byte_freq.get(byte, 0) + 1
    
    # Look for unusual patterns
    common_bytes = sorted(byte_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    print("Most common bytes:")
    for byte_val, count in common_bytes:
        print(f"  0x{byte_val:02X} ({chr(byte_val) if 32 <= byte_val <= 126 else '?'}): {count} times")
    
    # Method 6: Search for embedded files or data structures
    print("\n--- Method 6: Embedded Data Search ---")
    
    # Look for ZIP headers
    zip_pos = data.find(b'PK\x03\x04')
    if zip_pos != -1:
        print(f"Found ZIP header at position {zip_pos}")
    
    # Look for PNG headers
    png_pos = data.find(b'\x89PNG')
    if png_pos != -1:
        print(f"Found PNG header at position {png_pos}")
    
    # Look for JSON structures
    try:
        for i in range(len(data) - 10):
            if data[i:i+2] == b'{"':
                try:
                    json_data = data[i:].decode('utf-8')
                    json_obj = json.loads(json_data)
                    print(f"Found JSON at position {i}: {str(json_obj)[:100]}")
                except:
                    pass
    except:
        pass
    
    # Method 7: Look for specific Saleae data patterns
    print("\n--- Method 7: Saleae Data Pattern Analysis ---")
    
    # Extract potential signal data after header
    header_pos = data.find(b'<SALEAE>')
    if header_pos != -1:
        signal_data = data[header_pos + 8:]
        print(f"Signal data size: {len(signal_data)} bytes")
        
        # Try to interpret as timestamp + value pairs
        samples = []
        pos = 0
        while pos < len(signal_data) - 12:
            try:
                timestamp = struct.unpack('<Q', signal_data[pos:pos+8])[0]
                value = signal_data[pos+8]
                samples.append((timestamp, value))
                pos += 12  # Skip potential padding
            except:
                break
        
        print(f"Extracted {len(samples)} samples")
        
        if samples:
            # Look for UART patterns in samples
            uart_text = analyze_uart_samples(samples)
            if uart_text:
                print(f"UART analysis result: {repr(uart_text)}")
                results.append(uart_text)
    
    return results

def decode_uart_bits(data, baud_rate, bit_order):
    """Decode UART from raw bits"""
    # This is a simplified UART decoder
    # In reality, we'd need proper timing analysis
    
    # Look for start bits (0) followed by data bits
    bits = []
    for byte in data:
        for i in range(8):
            if bit_order == 'lsb':
                bit = (byte >> i) & 1
            else:
                bit = (byte >> (7-i)) & 1
            bits.append(bit)
    
    # Find start bits and decode characters
    chars = []
    i = 0
    while i < len(bits) - 10:
        if bits[i] == 0:  # Start bit
            char_bits = bits[i+1:i+9]
            if len(char_bits) == 8:
                char_value = 0
                for j, bit in enumerate(char_bits):
                    char_value |= (bit << j)
                
                if 32 <= char_value <= 126:
                    chars.append(chr(char_value))
                i += 10  # Skip start + 8 data + stop bit
            else:
                i += 1
        else:
            i += 1
    
    return ''.join(chars)

def analyze_uart_samples(samples):
    """Analyze samples for UART communication"""
    if not samples:
        return None
    
    # Find signal transitions
    transitions = []
    for i in range(1, len(samples)):
        if samples[i-1][1] != samples[i][1]:
            transitions.append((samples[i][0], samples[i][1]))
    
    # Look for UART start bits (high to low transition)
    chars = []
    for i in range(len(transitions) - 10):
        if transitions[i][1] == 0:  # Low signal
            # Check if previous was high
            if i > 0 and transitions[i-1][1] == 1:
                # Potential start bit
                # Try to decode 8 data bits
                char_bits = []
                for j in range(8):
                    if i + 1 + j < len(transitions):
                        char_bits.append(transitions[i + 1 + j][1])
                
                if len(char_bits) == 8:
                    char_value = 0
                    for k, bit in enumerate(char_bits):
                        char_value |= (bit << k)
                    
                    if 32 <= char_value <= 126:
                        chars.append(chr(char_value))
    
    return ''.join(chars)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 final_decoder.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    results = extract_all_text_methods(filename)
    
    print(f"\n=== FINAL RESULTS ===")
    if results:
        for i, result in enumerate(results):
            print(f"Result {i+1}: {result}")
            
            # Check if this looks like a flag
            if any(keyword in result.lower() for keyword in ['htb{', 'flag{', 'debug']):
                print(f"*** POTENTIAL FLAG: {result} ***")
    else:
        print("No text patterns found")

if __name__ == "__main__":
    main()