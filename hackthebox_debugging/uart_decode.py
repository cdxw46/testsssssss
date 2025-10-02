#!/usr/bin/env python3

import struct
import sys
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

# Set timeout for the entire script
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(15)  # 15 second timeout

def uart_decode(filename):
    """Try to decode the data as UART or similar serial protocol"""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            
        print(f"File size: {len(data)} bytes")
        
        # Skip the header and metadata
        header_size = 0x3a
        data_start = data[header_size:]
        
        # The data seems to contain patterns that might represent digital signals
        # Let's try to extract the actual signal data
        
        # Look for the pattern we observed in hexdump
        # Pattern: 00 00 00 80 XX 00 00 00 where XX is our value
        signal_values = []
        i = 0
        while i < len(data_start) - 8:
            # Check for pattern: 00 00 00 80 XX 00 00 00
            if (data_start[i] == 0x00 and data_start[i+1] == 0x00 and data_start[i+2] == 0x00 and 
                data_start[i+3] == 0x80 and data_start[i+5] == 0x00 and data_start[i+6] == 0x00 and 
                data_start[i+7] == 0x00):
                
                val = data_start[i+4]
                signal_values.append(val)
            i += 1
        
        print(f"Extracted {len(signal_values)} signal values")
        
        if signal_values:
            print("Signal values (first 50):")
            for i, val in enumerate(signal_values[:50]):
                print(f"{i:2d}: 0x{val:02x} ({val:3d}) {'*' if 32 <= val <= 126 else ''}")
            
            # Try to interpret as UART data
            # Look for start bits and decode bytes
            decoded_bytes = []
            i = 0
            while i < len(signal_values) - 8:
                # Look for potential start bit (0) followed by data bits
                if signal_values[i] == 0:  # Start bit
                    # Try to decode the next 8 bits as data
                    byte_val = 0
                    for bit_pos in range(8):
                        if i + 1 + bit_pos < len(signal_values):
                            bit_val = signal_values[i + 1 + bit_pos]
                            if bit_val == 1:
                                byte_val |= (1 << bit_pos)
                    
                    if byte_val != 0:  # Skip null bytes
                        decoded_bytes.append(byte_val)
                        print(f"Decoded byte: 0x{byte_val:02x} ('{chr(byte_val) if 32 <= byte_val <= 126 else '.'}')")
                    
                    i += 9  # Skip start bit + 8 data bits + stop bit
                else:
                    i += 1
            
            if decoded_bytes:
                text = ''.join(chr(b) for b in decoded_bytes if 32 <= b <= 126)
                print(f"\nDecoded text: {text}")
                
                # Look for flag pattern
                if 'HTB{' in text or 'flag' in text.lower():
                    print(f"*** POTENTIAL FLAG FOUND: {text} ***")
        
        # Also try a different approach - look at the raw byte values
        print(f"\nTrying raw byte analysis...")
        
        # Extract all non-zero bytes that might be data
        data_bytes = []
        for i, byte in enumerate(data_start):
            if byte != 0 and 0x20 <= byte <= 0x7E:  # Printable ASCII, non-zero
                data_bytes.append(byte)
        
        if data_bytes:
            print(f"Found {len(data_bytes)} printable non-zero bytes")
            text2 = ''.join(chr(b) for b in data_bytes)
            print(f"Raw text: {text2}")
            
            # Look for flag pattern
            if 'HTB{' in text2 or 'flag' in text2.lower():
                print(f"*** POTENTIAL FLAG FOUND: {text2} ***")
        
        # Try to find patterns that might be the flag
        print(f"\nLooking for flag patterns...")
        
        # Look for sequences that might be encoded flags
        # The sequences we found earlier might be parts of the flag
        sequences = [
            "F20>3g+RO",
            "NT:pp$#+_~c|L3", 
            "DGk4=SfQ7Z|Gx",
            "E6=F=^m$SK",
            "HsEw5*aWKy{IcPn}",
            "K^z8p zo\"0M#",
            "CXV=+@H{0IHh",
            "Se?4)<wP8m3vE",
            "A@|9;iQrXeC"
        ]
        
        # Try to combine these sequences in different ways
        print("Trying to combine sequences...")
        
        # Try concatenating them
        combined = ''.join(sequences)
        print(f"Combined: {combined}")
        
        # Try to find if any of these sequences contain the flag
        for seq in sequences:
            if '{' in seq and '}' in seq:
                print(f"Sequence with braces: {seq}")
                
        # Look for any sequence that might be base64 encoded
        import base64
        for seq in sequences:
            try:
                # Add padding
                padded = seq + '=' * (4 - len(seq) % 4)
                decoded = base64.b64decode(padded)
                decoded_text = decoded.decode('utf-8', errors='ignore')
                print(f"Base64 decode of '{seq}': {decoded_text}")
            except:
                pass
                
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 uart_decode.py <digital_file>")
        sys.exit(1)
    
    uart_decode(sys.argv[1])