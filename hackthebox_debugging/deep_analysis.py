#!/usr/bin/env python3

import struct
import sys
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

# Set timeout for the entire script
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(15)  # 15 second timeout

def deep_analysis(filename):
    """Deep analysis of the Saleae file"""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            
        print(f"File size: {len(data)} bytes")
        
        # Skip the header and metadata
        header_size = 0x3a  # From hexdump, data starts around here
        data_start = data[header_size:]
        
        print(f"Data section size: {len(data_start)} bytes")
        
        # Look for all 4-byte little-endian values that could be ASCII
        ascii_values = []
        for i in range(0, len(data_start) - 4, 4):
            val = struct.unpack('<I', data_start[i:i+4])[0]
            if 0x20 <= val <= 0x7E:  # Printable ASCII
                ascii_values.append(val)
                print(f"Offset 0x{i+header_size:x}: 0x{val:02x} ('{chr(val)}')")
        
        if ascii_values:
            text = ''.join(chr(v) for v in ascii_values)
            print(f"\nAll ASCII values: {text}")
            
            # Look for flag pattern
            if 'HTB{' in text or 'flag' in text.lower():
                print(f"*** POTENTIAL FLAG FOUND: {text} ***")
        
        # Also try looking at the raw bytes for patterns
        print("\nLooking for byte patterns...")
        byte_values = []
        for i, byte in enumerate(data_start):
            if 0x20 <= byte <= 0x7E:
                byte_values.append(byte)
                if len(byte_values) <= 20:  # Show first 20
                    print(f"Byte at 0x{i+header_size:x}: 0x{byte:02x} ('{chr(byte)}')")
        
        if byte_values:
            text2 = ''.join(chr(b) for b in byte_values)
            print(f"\nByte-level ASCII: {text2}")
            
            if 'HTB{' in text2 or 'flag' in text2.lower():
                print(f"*** POTENTIAL FLAG FOUND: {text2} ***")
        
        # Try to find the actual digital signal data
        print("\nLooking for digital signal patterns...")
        # The pattern we saw suggests this might be compressed or encoded data
        # Let's look for repeating patterns
        
        # Look for the specific pattern from hexdump: 80 19 00 00 00 00 00 80
        pattern = b'\x80\x19\x00\x00\x00\x00\x00\x80'
        pattern_positions = []
        pos = 0
        while True:
            pos = data.find(pattern, pos)
            if pos == -1:
                break
            pattern_positions.append(pos)
            pos += 1
        
        print(f"Found pattern at {len(pattern_positions)} positions")
        
        # Extract values that appear after this pattern
        extracted_values = []
        for pos in pattern_positions:
            if pos + 8 < len(data):
                # Look at the next few bytes after the pattern
                next_bytes = data[pos+8:pos+16]
                for byte in next_bytes:
                    if 0x20 <= byte <= 0x7E:
                        extracted_values.append(byte)
        
        if extracted_values:
            text3 = ''.join(chr(b) for b in extracted_values)
            print(f"Values after pattern: {text3}")
            
            if 'HTB{' in text3 or 'flag' in text3.lower():
                print(f"*** POTENTIAL FLAG FOUND: {text3} ***")
                
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 deep_analysis.py <digital_file>")
        sys.exit(1)
    
    deep_analysis(sys.argv[1])