#!/usr/bin/env python3

import struct
import sys
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

# Set timeout for the entire script
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)  # 10 second timeout

def get_final_flag(filename):
    """Get the final flag"""
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
        
        # Search for the sequence we found
        search_sequence = "HsEw5*aWKy{IcPn}"
        
        print(f"Searching for: {search_sequence}")
        
        if search_sequence in text:
            print(f"✓ Found flag sequence: {search_sequence}")
            pos = text.find(search_sequence)
            context = text[max(0, pos-20):pos+len(search_sequence)+20]
            print(f"Context: {context}")
            
            # Format as HTB flag
            formatted_flag = f"HTB{{{search_sequence[1:-1]}}}"  # Remove H and last }
            print(f"\n🎯 FINAL FLAG: {formatted_flag}")
            print(f"🎯 RAW SEQUENCE: {search_sequence}")
            
        else:
            print("❌ Flag sequence not found")
            
            # Try to find the sequence without the H
            search_sequence2 = "sEw5*aWKy{IcPn}"
            if search_sequence2 in text:
                print(f"✓ Found sequence without H: {search_sequence2}")
                pos = text.find(search_sequence2)
                context = text[max(0, pos-20):pos+len(search_sequence2)+20]
                print(f"Context: {context}")
                
                # Format as HTB flag
                formatted_flag = f"HTB{{{search_sequence2}}}"
                print(f"\n🎯 FINAL FLAG: {formatted_flag}")
                print(f"🎯 RAW SEQUENCE: {search_sequence2}")
            else:
                print("❌ Neither sequence found")
                
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 get_final_flag.py <digital_file>")
        sys.exit(1)
    
    get_final_flag(sys.argv[1])