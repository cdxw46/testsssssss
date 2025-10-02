#!/usr/bin/env python3

import struct
import sys
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

# Set timeout for the entire script
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)  # 10 second timeout

def analyze_saleae_file(filename):
    """Analyze Saleae file and extract potential data"""
    try:
        with open(filename, 'rb') as f:
            # Read header
            header = f.read(8)
            if header != b'<SALEAE>':
                print("Not a valid Saleae file")
                return
            
            print("Valid Saleae file found")
            
            # Read version
            version = struct.unpack('<I', f.read(4))[0]
            print(f"Version: {version}")
            
            # Read data size
            data_size = struct.unpack('<I', f.read(4))[0]
            print(f"Data size: {data_size}")
            
            # Read more metadata
            f.read(8)  # Skip some bytes
            
            # Read sample rate
            sample_rate = struct.unpack('<d', f.read(8))[0]
            print(f"Sample rate: {sample_rate}")
            
            # Read the rest of the file
            data = f.read()
            print(f"Data length: {len(data)} bytes")
            
            # Look for patterns in the data
            print("\nAnalyzing data patterns...")
            
            # Extract potential byte values from the pattern we saw
            potential_bytes = []
            i = 0
            while i < len(data) - 4:
                # Look for the pattern we observed
                if data[i:i+4] == b'\x00\x00\x00\x80':
                    # Check if next 4 bytes look like a value
                    val_bytes = data[i+4:i+8]
                    if len(val_bytes) == 4:
                        val = struct.unpack('<I', val_bytes)[0]
                        if 0x20 <= val <= 0x7E:  # Printable ASCII range
                            potential_bytes.append(val)
                            print(f"Found potential byte: 0x{val:02x} ('{chr(val)}')")
                i += 1
            
            # Try to decode as text
            if potential_bytes:
                print(f"\nExtracted {len(potential_bytes)} potential bytes")
                text = ''.join(chr(b) for b in potential_bytes)
                print(f"Decoded text: {text}")
                
                # Look for flag pattern
                if 'HTB{' in text or 'flag' in text.lower():
                    print(f"*** POTENTIAL FLAG FOUND: {text} ***")
            
            # Also try a different approach - look for all printable bytes
            print("\nTrying alternative approach...")
            all_bytes = []
            for i in range(0, len(data), 4):
                if i + 4 <= len(data):
                    val = struct.unpack('<I', data[i:i+4])[0]
                    if 0x20 <= val <= 0x7E:
                        all_bytes.append(val)
            
            if all_bytes:
                text2 = ''.join(chr(b) for b in all_bytes)
                print(f"Alternative decode: {text2}")
                
                if 'HTB{' in text2 or 'flag' in text2.lower():
                    print(f"*** POTENTIAL FLAG FOUND: {text2} ***")
                    
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_saleae.py <digital_file>")
        sys.exit(1)
    
    analyze_saleae_file(sys.argv[1])