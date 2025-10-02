#!/usr/bin/env python3

import struct
import sys
import signal
import re

def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

# Set timeout for the entire script
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(15)  # 15 second timeout

def extract_flag(filename):
    """Extract and analyze potential flag data"""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            
        print(f"File size: {len(data)} bytes")
        
        # Skip the header and metadata
        header_size = 0x3a
        data_start = data[header_size:]
        
        # Extract all printable ASCII characters
        ascii_chars = []
        for i, byte in enumerate(data_start):
            if 0x20 <= byte <= 0x7E:  # Printable ASCII
                ascii_chars.append(byte)
        
        text = ''.join(chr(b) for b in ascii_chars)
        print(f"Extracted text length: {len(text)}")
        
        # Look for patterns that might be encoded data
        # Look for sequences that look like base64 or other encodings
        potential_encoded = []
        
        # Find sequences of printable characters that might be encoded
        for match in re.finditer(r'[A-Za-z0-9+/=]{10,}', text):
            potential_encoded.append(match.group())
        
        print(f"Found {len(potential_encoded)} potential encoded sequences:")
        for i, seq in enumerate(potential_encoded[:10]):  # Show first 10
            print(f"{i+1}: {seq}")
        
        # Look for flag patterns
        flag_patterns = [
            r'HTB\{[^}]+\}',
            r'flag\{[^}]+\}',
            r'FLAG\{[^}]+\}',
            r'[A-Za-z0-9+/=]{20,}',  # Long base64-like strings
        ]
        
        for pattern in flag_patterns:
            matches = re.findall(pattern, text)
            if matches:
                print(f"\nFound matches for pattern {pattern}:")
                for match in matches:
                    print(f"  {match}")
        
        # Try to decode base64 sequences
        import base64
        for seq in potential_encoded:
            if len(seq) >= 20:  # Only try longer sequences
                try:
                    decoded = base64.b64decode(seq + '==')  # Add padding
                    decoded_text = decoded.decode('utf-8', errors='ignore')
                    if any(keyword in decoded_text.lower() for keyword in ['flag', 'htb', 'key', 'password']):
                        print(f"\nBase64 decode of '{seq[:20]}...': {decoded_text}")
                except:
                    pass
        
        # Look for specific patterns in the text
        print(f"\nLooking for specific patterns in the text...")
        
        # Find sequences that might be the flag
        # Look for sequences that contain common flag characters
        flag_candidates = []
        words = text.split()
        for word in words:
            if len(word) > 10 and any(c in word for c in '{}_'):
                flag_candidates.append(word)
        
        if flag_candidates:
            print("Flag candidates:")
            for candidate in flag_candidates:
                print(f"  {candidate}")
        
        # Also look for sequences that might be hex encoded
        hex_pattern = r'[0-9a-fA-F]{20,}'
        hex_matches = re.findall(hex_pattern, text)
        if hex_matches:
            print(f"\nFound {len(hex_matches)} hex-like sequences:")
            for match in hex_matches[:5]:  # Show first 5
                print(f"  {match}")
                try:
                    decoded = bytes.fromhex(match).decode('utf-8', errors='ignore')
                    if any(keyword in decoded.lower() for keyword in ['flag', 'htb', 'key']):
                        print(f"    Decoded: {decoded}")
                except:
                    pass
                    
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 extract_flag.py <digital_file>")
        sys.exit(1)
    
    extract_flag(sys.argv[1])