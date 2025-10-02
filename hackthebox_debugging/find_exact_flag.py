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

def find_exact_flag(filename):
    """Find the exact flag sequence in the data"""
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
        
        print(f"Total text length: {len(text)}")
        
        # Look for sequences with braces
        print(f"\nLooking for sequences with braces...")
        brace_pattern = r'\{[^}]+\}'
        brace_matches = re.findall(brace_pattern, text)
        
        if brace_matches:
            print(f"Found {len(brace_matches)} sequences with braces:")
            for i, match in enumerate(brace_matches):
                print(f"{i+1}: {match}")
        
        # Look for sequences that contain the pattern we saw
        print(f"\nLooking for sequences containing 'sEw5*aWKy'...")
        if 'sEw5*aWKy' in text:
            print("✓ Found 'sEw5*aWKy' in text")
            # Find the context around it
            pos = text.find('sEw5*aWKy')
            context = text[max(0, pos-20):pos+30]
            print(f"Context: {context}")
        
        # Look for sequences that look like flags
        print(f"\nLooking for flag-like patterns...")
        
        # Pattern for HTB flags
        htb_pattern = r'HTB\{[^}]+\}'
        htb_matches = re.findall(htb_pattern, text)
        if htb_matches:
            print(f"HTB flags found: {htb_matches}")
        
        # Pattern for any sequence with braces that might be a flag
        flag_pattern = r'[A-Za-z0-9*+_~|<>#@$^&()=]{3,}\{[A-Za-z0-9*+_~|<>#@$^&()=]{3,}\}'
        flag_matches = re.findall(flag_pattern, text)
        if flag_matches:
            print(f"Flag-like sequences found:")
            for match in flag_matches:
                print(f"  {match}")
        
        # Look for the specific sequences we found earlier
        sequences = [
            "HsEw5*aWKy{IcPn}",
            "sEw5*aWKy{IcPn}",
            "Ew5*aWKy{IcPn}",
            "w5*aWKy{IcPn}",
            "5*aWKy{IcPn}",
            "*aWKy{IcPn}",
            "aWKy{IcPn}",
            "WKy{IcPn}",
            "Ky{IcPn}",
            "y{IcPn}",
            "{IcPn}",
            "IcPn",
            "cPn",
            "Pn",
            "n"
        ]
        
        print(f"\nChecking for partial matches...")
        for seq in sequences:
            if seq in text:
                print(f"✓ Found: {seq}")
                pos = text.find(seq)
                context = text[max(0, pos-10):pos+len(seq)+10]
                print(f"  Context: {context}")
        
        # Look for any sequence that contains both { and }
        print(f"\nLooking for any sequence with both braces...")
        brace_pairs = re.findall(r'[^{]*\{[^}]*\}[^{]*', text)
        if brace_pairs:
            print(f"Found {len(brace_pairs)} sequences with brace pairs:")
            for i, match in enumerate(brace_pairs[:10]):  # Show first 10
                print(f"{i+1}: {match}")
        
        # Look for sequences that might be encoded
        print(f"\nLooking for encoded sequences...")
        encoded_pattern = r'[A-Za-z0-9*+_~|<>#@$^&()=]{8,}'
        encoded_matches = re.findall(encoded_pattern, text)
        
        # Filter for sequences that look like they might be flags
        potential_flags = []
        for match in encoded_matches:
            if '{' in match and '}' in match and len(match) > 10:
                potential_flags.append(match)
        
        if potential_flags:
            print(f"Potential flag sequences:")
            for flag in potential_flags:
                print(f"  {flag}")
                
    except TimeoutError:
        print("Script timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 find_exact_flag.py <digital_file>")
        sys.exit(1)
    
    find_exact_flag(sys.argv[1])