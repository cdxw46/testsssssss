#!/usr/bin/env python3

import struct
import sys
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

# Set timeout for the entire script
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)  # 10 second timeout

def search_exact(filename):
    """Search for the exact flag sequence"""
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
        
        # Search for the exact sequence we found
        search_sequence = "sEw5*aWKy{IcPn}"
        
        print(f"Searching for: {search_sequence}")
        print(f"Text length: {len(text)}")
        
        if search_sequence in text:
            print(f"✓ Found exact sequence: {search_sequence}")
            pos = text.find(search_sequence)
            context = text[max(0, pos-30):pos+len(search_sequence)+30]
            print(f"Context: {context}")
        else:
            print("❌ Exact sequence not found")
            
            # Try to find similar sequences
            print(f"\nLooking for similar sequences...")
            
            # Look for sequences with the pattern
            if "sEw5" in text:
                print("✓ Found 'sEw5'")
                pos = text.find("sEw5")
                context = text[max(0, pos-10):pos+50]
                print(f"Context: {context}")
            
            if "aWKy" in text:
                print("✓ Found 'aWKy'")
                pos = text.find("aWKy")
                context = text[max(0, pos-10):pos+20]
                print(f"Context: {context}")
            
            if "IcPn" in text:
                print("✓ Found 'IcPn'")
                pos = text.find("IcPn")
                context = text[max(0, pos-10):pos+20]
                print(f"Context: {context}")
            
            # Look for any sequence with braces
            import re
            brace_pattern = r'\{[^}]+\}'
            brace_matches = re.findall(brace_pattern, text)
            if brace_matches:
                print(f"\nFound {len(brace_matches)} sequences with braces:")
                for i, match in enumerate(brace_matches[:5]):  # Show first 5
                    print(f"{i+1}: {match}")
            
            # Look for sequences that might be the flag
            flag_pattern = r'[A-Za-z0-9*+_~|<>#@$^&()=]{5,}\{[A-Za-z0-9*+_~|<>#@$^&()=]{3,}\}'
            flag_matches = re.findall(flag_pattern, text)
            if flag_matches:
                print(f"\nFound {len(flag_matches)} flag-like sequences:")
                for i, match in enumerate(flag_matches[:10]):  # Show first 10
                    print(f"{i+1}: {match}")
                    
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 search_exact.py <digital_file>")
        sys.exit(1)
    
    search_exact(sys.argv[1])