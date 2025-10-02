#!/usr/bin/env python3

import struct
import sys
import signal
import re
import base64

def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

# Set timeout for the entire script
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(20)  # 20 second timeout

def alternative_approach(filename):
    """Alternative approach to find the flag"""
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
        
        # Look for sequences that might be the flag
        print(f"\n=== LOOKING FOR FLAG CANDIDATES ===")
        
        # Look for sequences that contain common flag characters
        flag_chars = '{}_'
        sequences_with_flag_chars = []
        
        # Split text into words and look for sequences with flag characters
        words = text.split()
        for word in words:
            if any(char in word for char in flag_chars) and len(word) > 5:
                sequences_with_flag_chars.append(word)
        
        if sequences_with_flag_chars:
            print(f"Sequences with flag characters:")
            for seq in sequences_with_flag_chars:
                print(f"  {seq}")
        
        # Look for sequences that might be base64 encoded
        print(f"\n=== TRYING BASE64 DECODING ===")
        
        # Look for long sequences that might be base64
        base64_pattern = r'[A-Za-z0-9+/=]{16,}'
        base64_matches = re.findall(base64_pattern, text)
        
        print(f"Found {len(base64_matches)} potential base64 sequences")
        for i, match in enumerate(base64_matches[:30]):  # Show first 30
            try:
                # Add padding
                padded = match + '=' * (4 - len(match) % 4)
                decoded = base64.b64decode(padded)
                decoded_text = decoded.decode('utf-8', errors='ignore')
                
                # Check if it contains flag-like content
                if any(keyword in decoded_text.lower() for keyword in ['flag', 'htb', 'key', 'password', 'secret']):
                    print(f"{i+1}: {match[:40]}... -> {decoded_text}")
                elif len(decoded_text) > 10 and all(ord(c) < 128 for c in decoded_text):
                    print(f"{i+1}: {match[:40]}... -> {decoded_text}")
            except:
                pass
        
        # Look for sequences that might be hex encoded
        print(f"\n=== TRYING HEX DECODING ===")
        
        hex_pattern = r'[0-9a-fA-F]{16,}'
        hex_matches = re.findall(hex_pattern, text)
        
        print(f"Found {len(hex_matches)} potential hex sequences")
        for i, match in enumerate(hex_matches[:20]):  # Show first 20
            try:
                decoded = bytes.fromhex(match)
                decoded_text = decoded.decode('utf-8', errors='ignore')
                
                if any(keyword in decoded_text.lower() for keyword in ['flag', 'htb', 'key', 'password', 'secret']):
                    print(f"{i+1}: {match[:40]}... -> {decoded_text}")
                elif len(decoded_text) > 5 and all(ord(c) < 128 for c in decoded_text):
                    print(f"{i+1}: {match[:40]}... -> {decoded_text}")
            except:
                pass
        
        # Look for sequences that might be the flag in different formats
        print(f"\n=== LOOKING FOR DIFFERENT FLAG FORMATS ===")
        
        # Look for sequences that start with common prefixes
        prefixes = ['HTB', 'htb', 'FLAG', 'flag', 'FLG', 'flg']
        for prefix in prefixes:
            if prefix in text:
                print(f"Found prefix: {prefix}")
                pos = text.find(prefix)
                # Extract context around it
                context = text[max(0, pos-10):pos+50]
                print(f"  Context: {context}")
        
        # Look for sequences that might be the flag without braces
        print(f"\n=== LOOKING FOR FLAG WITHOUT BRACES ===")
        
        # Look for sequences that might be the flag content
        flag_content_patterns = [
            r'[A-Za-z0-9*+_~|<>#@$^&()=]{8,}',
            r'[A-Za-z0-9]{8,}',
            r'[A-Za-z0-9*+_~|<>#@$^&()=]{5,}'
        ]
        
        for pattern in flag_content_patterns:
            matches = re.findall(pattern, text)
            print(f"Pattern {pattern}: found {len(matches)} matches")
            
            # Show some interesting ones
            for i, match in enumerate(matches[:10]):
                if len(match) > 8:
                    print(f"  {i+1}: {match}")
        
        # Try to find sequences that might be the flag by looking for common patterns
        print(f"\n=== LOOKING FOR COMMON FLAG PATTERNS ===")
        
        # Look for sequences that might be the flag
        potential_flags = []
        
        # Look for sequences that contain both letters and numbers
        mixed_pattern = r'[A-Za-z0-9*+_~|<>#@$^&()=]{10,}'
        mixed_matches = re.findall(mixed_pattern, text)
        
        for match in mixed_matches:
            if len(match) > 10 and any(c.isalpha() for c in match) and any(c.isdigit() for c in match):
                potential_flags.append(match)
        
        if potential_flags:
            print(f"Potential flag sequences:")
            for i, flag in enumerate(potential_flags[:20]):  # Show first 20
                print(f"{i+1}: {flag}")
        
        # Try to find the flag by looking for sequences that might be encoded
        print(f"\n=== TRYING TO DECODE SPECIFIC SEQUENCES ===")
        
        # The sequences we found earlier
        sequences_to_try = [
            "F20>3g+RO",
            "NT:pp$#+_~c|L3", 
            "DGk4=SfQ7Z|Gx",
            "E6=F=^m$SK",
            "K^z8p zo\"0M#",
            "CXV=+@H{0IHh",
            "Se?4)<wP8m3vE",
            "A@|9;iQrXeC"
        ]
        
        for seq in sequences_to_try:
            if seq in text:
                print(f"\nAnalyzing sequence: {seq}")
                
                # Try different decoding methods
                try:
                    # Base64
                    padded = seq + '=' * (4 - len(seq) % 4)
                    decoded = base64.b64decode(padded)
                    decoded_text = decoded.decode('utf-8', errors='ignore')
                    print(f"  Base64: {decoded_text}")
                except:
                    pass
                
                try:
                    # Hex
                    hex_chars = ''.join(c for c in seq if c in '0123456789ABCDEFabcdef')
                    if len(hex_chars) % 2 == 0 and len(hex_chars) > 0:
                        decoded = bytes.fromhex(hex_chars)
                        decoded_text = decoded.decode('utf-8', errors='ignore')
                        print(f"  Hex: {decoded_text}")
                except:
                    pass
                
                # ROT13
                try:
                    rot13 = seq.translate(str.maketrans(
                        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                        'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
                    ))
                    print(f"  ROT13: {rot13}")
                except:
                    pass
                
                # Try Caesar cipher
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
                            print(f"  Caesar +{shift}: {caesar}")
                    except:
                        pass
                
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 alternative_approach.py <digital_file>")
        sys.exit(1)
    
    alternative_approach(sys.argv[1])