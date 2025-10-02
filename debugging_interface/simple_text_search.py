#!/usr/bin/env python3

import sys
import re

def search_text_patterns(filename):
    """Search for text patterns in binary file"""
    print(f"Searching for text patterns in {filename}")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
    # Search for common flag patterns
    flag_patterns = [
        b'HTB{',
        b'flag{',
        b'FLAG{',
        b'ctf{',
        b'CTF{',
        b'HTB_',
        b'hackthebox',
        b'HackTheBox'
    ]
    
    print("\nSearching for flag patterns:")
    for pattern in flag_patterns:
        matches = []
        start = 0
        while True:
            pos = data.find(pattern, start)
            if pos == -1:
                break
            matches.append(pos)
            start = pos + 1
        
        if matches:
            print(f"Found '{pattern.decode()}' at positions: {matches}")
            for pos in matches:
                # Extract surrounding context
                start = max(0, pos - 20)
                end = min(len(data), pos + 50)
                context = data[start:end]
                print(f"  Context: {context}")
    
    # Search for printable ASCII sequences
    print("\nSearching for printable ASCII sequences:")
    ascii_pattern = re.compile(b'[ -~]{4,}')
    matches = ascii_pattern.findall(data)
    
    for match in matches[:20]:  # Show first 20 matches
        if len(match) >= 4:
            print(f"  ASCII sequence: {match}")
    
    # Search for repeated patterns
    print("\nSearching for repeated byte patterns:")
    pattern_counts = {}
    for i in range(len(data) - 3):
        pattern = data[i:i+4]
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
    
    # Show most common patterns
    sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
    for pattern, count in sorted_patterns[:10]:
        if count > 5:  # Only show patterns that appear more than 5 times
            print(f"  Pattern {pattern} appears {count} times")
    
    # Try to find any text that might be encoded differently
    print("\nTrying different interpretations:")
    
    # Try interpreting as different data types
    for offset in [0, 8, 16, 32]:
        print(f"\nOffset {offset}:")
        chunk = data[offset:offset+100]
        
        # Try as ASCII
        ascii_text = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        if any(c.isalpha() for c in ascii_text):
            print(f"  ASCII: {ascii_text}")
        
        # Try as hex
        hex_text = chunk.hex()
        print(f"  HEX: {hex_text[:50]}...")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 simple_text_search.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    search_text_patterns(filename)

if __name__ == "__main__":
    main()