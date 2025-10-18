#!/usr/bin/env python3
import re
import string

# Read the heap dump as binary
with open('/workspace/heapdump.hprof', 'rb') as f:
    data = f.read()

# Convert to string with latin-1 encoding to preserve all bytes
text = data.decode('latin-1', errors='ignore')

# Look for strings that could be flags
# CTFlearn{...} format
pattern1 = r'CTFlearn\{[^\}]{10,50}\}'
matches1 = re.findall(pattern1, text)
if matches1:
    print("Found CTFlearn{} format:")
    for m in matches1:
        print(m)

# Look for strings with mixed case and special chars that could be flags
# Length 30-50, contains letters and special chars
printable = set(string.printable) - set('\t\n\r\x0b\x0c')
possible_flags = []

# Split by null bytes and other non-printable chars
parts = re.split(r'[\x00-\x1f\x7f-\xff]+', text)
for part in parts:
    if 25 <= len(part) <= 60:
        # Check if it's mostly printable and has some variety
        if all(c in printable for c in part):
            # Skip if it looks like Java code
            if 'java' not in part.lower() and 'sun/' not in part:
                # Skip if it's all one type of character
                has_upper = any(c.isupper() for c in part)
                has_lower = any(c.islower() for c in part)
                has_digit = any(c.isdigit() for c in part)
                
                if (has_upper or has_lower) and not part.startswith('('):
                    # Check for specific keywords that might be in a flag
                    if any(word in part.lower() for word in ['heap', 'dump', 'memory', 'flag', 'easy', 'ctf']):
                        possible_flags.append(part)

print("\n\nPossible flags with keywords:")
for f in set(possible_flags):
    print(f)
