#!/usr/bin/env python3

import struct
import sys
import signal
import base64
import binascii

def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

# Set timeout for the entire script
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(15)  # 15 second timeout

def decode_sequences(filename):
    """Decode potential encoded sequences from the file"""
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
        
        # Look for specific sequences that might be encoded
        sequences = [
            "F20>3g+RO",
            "NT:pp$#+_~c|L3", 
            "DGk4=SfQ7Z|Gx",
            "E6=F=^m$SK",
            "HsEw5*aWKy{IcPn}",
            "K^z8p zo\"0M#",
            "CXV=+@H{0IHh",
            "Se?4)<wP8m3vE",
            "NT:pp$#+_~c|L3",
            "DGk4=SfQ7Z|Gx",
            "E6=F=^m$SK",
            "HsEw5*aWKy{IcPn}",
            "A@|9;iQrXeC",
            "E6=F=^m$SK"
        ]
        
        print("Analyzing potential encoded sequences...")
        
        for seq in sequences:
            if seq in text:
                print(f"\nFound sequence: {seq}")
                
                # Try different decoding methods
                print("  Trying different decodings:")
                
                # 1. Base64
                try:
                    # Add padding if needed
                    padded = seq + '=' * (4 - len(seq) % 4)
                    decoded = base64.b64decode(padded)
                    decoded_text = decoded.decode('utf-8', errors='ignore')
                    print(f"    Base64: {decoded_text}")
                except:
                    print("    Base64: Failed")
                
                # 2. Hex decode
                try:
                    # Remove non-hex characters
                    hex_chars = ''.join(c for c in seq if c in '0123456789ABCDEFabcdef')
                    if len(hex_chars) % 2 == 0 and len(hex_chars) > 0:
                        decoded = bytes.fromhex(hex_chars)
                        decoded_text = decoded.decode('utf-8', errors='ignore')
                        print(f"    Hex: {decoded_text}")
                except:
                    print("    Hex: Failed")
                
                # 3. ROT13
                try:
                    rot13 = seq.translate(str.maketrans(
                        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                        'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
                    ))
                    print(f"    ROT13: {rot13}")
                except:
                    print("    ROT13: Failed")
                
                # 4. Caesar cipher (try different shifts)
                for shift in range(1, 26):
                    try:
                        caesar = ''
                        for char in seq:
                            if char.isalpha():
                                if char.isupper():
                                    caesar += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                                else:
                                    caesar += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                            else:
                                caesar += char
                        if 'flag' in caesar.lower() or 'htb' in caesar.lower():
                            print(f"    Caesar +{shift}: {caesar}")
                    except:
                        pass
        
        # Also look for any sequences that might contain the flag
        print(f"\nLooking for flag patterns in the entire text...")
        
        # Look for sequences that might be the flag
        flag_patterns = [
            r'HTB\{[^}]+\}',
            r'flag\{[^}]+\}',
            r'FLAG\{[^}]+\}',
        ]
        
        import re
        for pattern in flag_patterns:
            matches = re.findall(pattern, text)
            if matches:
                print(f"Found flag pattern {pattern}: {matches}")
        
        # Look for sequences that look like they might be encoded flags
        # Look for sequences with curly braces
        brace_sequences = re.findall(r'\{[^}]+\}', text)
        if brace_sequences:
            print(f"\nFound sequences with braces: {brace_sequences}")
        
        # Look for sequences that might be base64 encoded flags
        base64_pattern = r'[A-Za-z0-9+/=]{20,}'
        base64_matches = re.findall(base64_pattern, text)
        
        print(f"\nTrying to decode base64-like sequences...")
        for match in base64_matches[:10]:  # Try first 10
            try:
                # Add padding
                padded = match + '=' * (4 - len(match) % 4)
                decoded = base64.b64decode(padded)
                decoded_text = decoded.decode('utf-8', errors='ignore')
                if any(keyword in decoded_text.lower() for keyword in ['flag', 'htb', 'key', 'password']):
                    print(f"  {match[:30]}... -> {decoded_text}")
            except:
                pass
                
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 decode_sequences.py <digital_file>")
        sys.exit(1)
    
    decode_sequences(sys.argv[1])