#!/usr/bin/env python3

import struct
import sys
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

# Set timeout for the entire script
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)  # 10 second timeout

def extract_values(filename):
    """Extract values from the hexdump pattern we observed"""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            
        print(f"File size: {len(data)} bytes")
        
        # Look for the specific pattern we saw in hexdump
        # Pattern: 00 00 00 80 XX 00 00 00 where XX is our value
        values = []
        i = 0
        while i < len(data) - 8:
            # Check for pattern: 00 00 00 80 XX 00 00 00
            if (data[i] == 0x00 and data[i+1] == 0x00 and data[i+2] == 0x00 and 
                data[i+3] == 0x80 and data[i+5] == 0x00 and data[i+6] == 0x00 and 
                data[i+7] == 0x00):
                
                val = data[i+4]
                if 0x20 <= val <= 0x7E:  # Printable ASCII
                    values.append(val)
                    print(f"Found value: 0x{val:02x} ('{chr(val)}') at offset 0x{i+4:x}")
            i += 1
        
        if values:
            print(f"\nExtracted {len(values)} values")
            text = ''.join(chr(v) for v in values)
            print(f"Decoded text: {text}")
            
            # Look for flag pattern
            if 'HTB{' in text or 'flag' in text.lower():
                print(f"*** POTENTIAL FLAG FOUND: {text} ***")
        
        # Also try looking for the values we saw directly: 0x33, 0x4c, 0x66, etc.
        print("\nLooking for specific values from hexdump...")
        specific_values = [0x33, 0x4c, 0x66, 0x7f, 0x99, 0xb2, 0xcc, 0xe5, 0xff]
        found_values = []
        
        for val in specific_values:
            if val in data:
                found_values.append(val)
                char = chr(val) if 0x20 <= val <= 0x7E else '.'
                print(f"Found 0x{val:02x} ('{char}')")
        
        if found_values:
            text2 = ''.join(chr(v) for v in found_values if 0x20 <= v <= 0x7E)
            print(f"Specific values text: {text2}")
            
            if 'HTB{' in text2 or 'flag' in text2.lower():
                print(f"*** POTENTIAL FLAG FOUND: {text2} ***")
                
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 extract_values.py <digital_file>")
        sys.exit(1)
    
    extract_values(sys.argv[1])