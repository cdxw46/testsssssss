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

def deep_analysis_v2(filename):
    """Deep analysis of the Saleae file - version 2"""
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
        
        # Look for all sequences with braces
        print(f"\n=== LOOKING FOR ALL BRACE SEQUENCES ===")
        brace_pattern = r'\{[^}]+\}'
        brace_matches = re.findall(brace_pattern, text)
        
        if brace_matches:
            print(f"Found {len(brace_matches)} sequences with braces:")
            for i, match in enumerate(brace_matches):
                print(f"{i+1}: {match}")
                
                # Try to decode each one
                try:
                    # Try base64
                    padded = match[1:-1] + '=' * (4 - len(match[1:-1]) % 4)
                    decoded = base64.b64decode(padded)
                    decoded_text = decoded.decode('utf-8', errors='ignore')
                    if any(keyword in decoded_text.lower() for keyword in ['flag', 'htb', 'key', 'password']):
                        print(f"  -> Base64: {decoded_text}")
                except:
                    pass
        
        # Look for sequences that might be flags
        print(f"\n=== LOOKING FOR FLAG PATTERNS ===")
        
        # HTB pattern
        htb_pattern = r'HTB\{[^}]+\}'
        htb_matches = re.findall(htb_pattern, text)
        if htb_matches:
            print(f"HTB flags found: {htb_matches}")
        
        # Any sequence with braces that looks like a flag
        flag_pattern = r'[A-Za-z0-9*+_~|<>#@$^&()=]{3,}\{[A-Za-z0-9*+_~|<>#@$^&()=]{3,}\}'
        flag_matches = re.findall(flag_pattern, text)
        if flag_matches:
            print(f"Flag-like sequences:")
            for match in flag_matches:
                print(f"  {match}")
        
        # Look for base64-like sequences
        print(f"\n=== LOOKING FOR BASE64-LIKE SEQUENCES ===")
        base64_pattern = r'[A-Za-z0-9+/=]{20,}'
        base64_matches = re.findall(base64_pattern, text)
        
        print(f"Found {len(base64_matches)} base64-like sequences")
        for i, match in enumerate(base64_matches[:20]):  # Show first 20
            try:
                padded = match + '=' * (4 - len(match) % 4)
                decoded = base64.b64decode(padded)
                decoded_text = decoded.decode('utf-8', errors='ignore')
                if any(keyword in decoded_text.lower() for keyword in ['flag', 'htb', 'key', 'password']):
                    print(f"{i+1}: {match[:30]}... -> {decoded_text}")
            except:
                pass
        
        # Look for hex patterns
        print(f"\n=== LOOKING FOR HEX PATTERNS ===")
        hex_pattern = r'[0-9a-fA-F]{20,}'
        hex_matches = re.findall(hex_pattern, text)
        
        print(f"Found {len(hex_matches)} hex-like sequences")
        for i, match in enumerate(hex_matches[:10]):  # Show first 10
            try:
                decoded = bytes.fromhex(match).decode('utf-8', errors='ignore')
                if any(keyword in decoded.lower() for keyword in ['flag', 'htb', 'key', 'password']):
                    print(f"{i+1}: {match[:30]}... -> {decoded}")
            except:
                pass
        
        # Look for any sequence that might contain the flag
        print(f"\n=== LOOKING FOR ANY INTERESTING SEQUENCES ===")
        
        # Look for sequences with common flag characters
        interesting_pattern = r'[A-Za-z0-9*+_~|<>#@$^&()=]{8,}'
        interesting_matches = re.findall(interesting_pattern, text)
        
        # Filter for sequences that might be flags
        potential_flags = []
        for match in interesting_matches:
            if len(match) > 10 and any(c in match for c in '{}_'):
                potential_flags.append(match)
        
        if potential_flags:
            print(f"Potentially interesting sequences:")
            for i, flag in enumerate(potential_flags[:20]):  # Show first 20
                print(f"{i+1}: {flag}")
        
        # Try to find the actual flag by looking for common patterns
        print(f"\n=== TRYING TO FIND THE ACTUAL FLAG ===")
        
        # Look for sequences that start with common flag prefixes
        prefixes = ['HTB{', 'flag{', 'FLAG{', 'htb{']
        for prefix in prefixes:
            if prefix in text:
                print(f"Found prefix: {prefix}")
                pos = text.find(prefix)
                # Extract the full flag
                end_pos = text.find('}', pos)
                if end_pos != -1:
                    full_flag = text[pos:end_pos+1]
                    print(f"  Full flag: {full_flag}")
        
        # Look for any sequence that might be encoded
        print(f"\n=== TRYING DIFFERENT DECODING METHODS ===")
        
        # Try to find sequences that might be the flag encoded
        sequences_to_try = [
            "F20>3g+RO",
            "NT:pp$#+_~c|L3", 
            "DGk4=SfQ7Z|Gx",
            "E6=F=^m$SK",
            "HsEw5*aWKy{IcPn}",
            "sEw5*aWKy{IcPn}",
            "K^z8p zo\"0M#",
            "CXV=+@H{0IHh",
            "Se?4)<wP8m3vE",
            "A@|9;iQrXeC"
        ]
        
        for seq in sequences_to_try:
            if seq in text:
                print(f"Found sequence: {seq}")
                
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
                
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 deep_analysis_v2.py <digital_file>")
        sys.exit(1)
    
    deep_analysis_v2(sys.argv[1])