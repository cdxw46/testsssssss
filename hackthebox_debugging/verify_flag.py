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

def verify_flag(filename):
    """Verify and extract the final flag"""
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
        
        # Look for the specific sequence we found
        flag_sequence = "HsEw5*aWKy{IcPn}"
        
        if flag_sequence in text:
            print(f"✓ Found flag sequence: {flag_sequence}")
            
            # Check if it needs to be formatted as HTB{...}
            if flag_sequence.startswith('H') and '{' in flag_sequence and '}' in flag_sequence:
                # It might already be the flag, or it might need HTB prefix
                if not flag_sequence.startswith('HTB{'):
                    formatted_flag = f"HTB{{{flag_sequence[1:-1]}}}"  # Remove H and last }, add HTB{
                    print(f"✓ Formatted flag: {formatted_flag}")
                else:
                    print(f"✓ Flag is already formatted: {flag_sequence}")
            
            # Also check if there are other similar sequences
            print(f"\nLooking for other flag-like sequences...")
            
            # Look for sequences with braces
            brace_pattern = r'[A-Za-z0-9*+_~|<>#@$^&()=]{5,}\{[A-Za-z0-9*+_~|<>#@$^&()=]{5,}\}'
            brace_matches = re.findall(brace_pattern, text)
            
            if brace_matches:
                print("Found sequences with braces:")
                for match in brace_matches:
                    print(f"  {match}")
            
            # Look for sequences that might be base64 encoded flags
            print(f"\nTrying base64 decoding of the flag sequence...")
            import base64
            try:
                # Try to decode the part inside the braces
                inner_part = flag_sequence[1:-1]  # Remove H and }
                # Add padding
                padded = inner_part + '=' * (4 - len(inner_part) % 4)
                decoded = base64.b64decode(padded)
                decoded_text = decoded.decode('utf-8', errors='ignore')
                print(f"Base64 decode of inner part: {decoded_text}")
            except:
                print("Base64 decode failed")
            
            # Try different interpretations
            print(f"\nTrying different interpretations...")
            
            # 1. As is
            print(f"1. As found: {flag_sequence}")
            
            # 2. With HTB prefix
            if not flag_sequence.startswith('HTB{'):
                htbf = f"HTB{{{flag_sequence[1:-1]}}}"
                print(f"2. With HTB prefix: {htbf}")
            
            # 3. Try ROT13
            try:
                rot13 = flag_sequence.translate(str.maketrans(
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                    'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
                ))
                print(f"3. ROT13: {rot13}")
            except:
                pass
            
            # 4. Try Caesar cipher
            for shift in range(1, 26):
                try:
                    caesar = ''
                    for char in flag_sequence:
                        if char.isalpha():
                            if char.isupper():
                                caesar += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                            else:
                                caesar += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                        else:
                            caesar += char
                    if 'flag' in caesar.lower() or 'htb' in caesar.lower():
                        print(f"4. Caesar +{shift}: {caesar}")
                except:
                    pass
            
            print(f"\n🎯 FINAL FLAG CANDIDATE: {flag_sequence}")
            if not flag_sequence.startswith('HTB{'):
                print(f"🎯 FORMATTED FLAG: HTB{{{flag_sequence[1:-1]}}}")
            
        else:
            print("❌ Flag sequence not found in the data")
            
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 verify_flag.py <digital_file>")
        sys.exit(1)
    
    verify_flag(sys.argv[1])