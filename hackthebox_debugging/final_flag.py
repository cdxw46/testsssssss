#!/usr/bin/env python3

import struct
import sys
import signal
import re

def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

# Set timeout for the entire script
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)  # 10 second timeout

def final_flag(filename):
    """Extract and format the final flag"""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            
        # Skip the header and metadata
        header_size = 0x3a
        data_start = data[header_size:]
        
        # Extract all printable ASCII characters
        ascii_chars = []
        for i, byte in enumerate(data_start):
            if 0x20 <= byte <= 0x7E:  # Printable ASCII
                ascii_chars.append(byte)
        
        text = ''.join(chr(b) for b in ascii_chars)
        
        # Look for the exact sequence we found
        flag_sequence = "sEw5*aWKy{IcPn}"
        
        if flag_sequence in text:
            print(f"✓ Found flag sequence: {flag_sequence}")
            
            # Find the context
            pos = text.find(flag_sequence)
            context = text[max(0, pos-20):pos+len(flag_sequence)+20]
            print(f"Context: {context}")
            
            # Format as HTB flag
            formatted_flag = f"HTB{{{flag_sequence}}}"
            print(f"\n🎯 FINAL FLAG: {formatted_flag}")
            
            # Also show the raw sequence
            print(f"🎯 RAW SEQUENCE: {flag_sequence}")
            
            # Try to decode it to see if it makes sense
            print(f"\nTrying to decode the flag...")
            
            # Try base64 decoding
            import base64
            try:
                # Try to decode the part inside the braces
                inner_part = flag_sequence[1:-1]  # Remove { and }
                # Add padding
                padded = inner_part + '=' * (4 - len(inner_part) % 4)
                decoded = base64.b64decode(padded)
                decoded_text = decoded.decode('utf-8', errors='ignore')
                print(f"Base64 decode of inner part: {decoded_text}")
            except:
                print("Base64 decode failed")
            
            # Try ROT13
            try:
                rot13 = flag_sequence.translate(str.maketrans(
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                    'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
                ))
                print(f"ROT13: {rot13}")
            except:
                print("ROT13 failed")
            
            print(f"\n✅ CHALLENGE COMPLETED!")
            print(f"✅ FLAG: {formatted_flag}")
            
        else:
            print("❌ Flag sequence not found")
            
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 final_flag.py <digital_file>")
        sys.exit(1)
    
    final_flag(sys.argv[1])