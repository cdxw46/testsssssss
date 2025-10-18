#!/usr/bin/env python3
import struct
import sys

def read_hprof(filename):
    with open(filename, 'rb') as f:
        # Read header
        header = f.readline()
        print(f"Header: {header}")
        
        # Skip rest of header
        id_size = struct.unpack('>I', f.read(4))[0]
        timestamp = struct.unpack('>Q', f.read(8))[0]
        
        print(f"ID Size: {id_size}, Timestamp: {timestamp}")
        
        strings_found = []
        
        # Read records
        while True:
            tag_byte = f.read(1)
            if not tag_byte:
                break
                
            tag = struct.unpack('B', tag_byte)[0]
            timestamp = struct.unpack('>I', f.read(4))[0]
            length_bytes = f.read(4)
            if not length_bytes:
                break
            length = struct.unpack('>I', length_bytes)[0]
            
            if tag == 0x01:  # UTF-8 String
                data = f.read(length)
                if length >= 8:  # Skip very short strings
                    str_id = struct.unpack('>Q', data[:8])[0] if len(data) >= 8 else 0
                    string_data = data[8:]
                    try:
                        decoded = string_data.decode('utf-8', errors='ignore')
                        if len(decoded) > 10 and len(decoded) < 100:
                            # Filter out Java internals
                            if not any(x in decoded for x in ['java/', 'sun/', 'javax/', 'Ljava']):
                                if '{' in decoded or 'CTF' in decoded or 'flag' in decoded.lower():
                                    print(f"Interesting string: {decoded}")
                                    strings_found.append(decoded)
                    except:
                        pass
            else:
                # Skip this record
                f.read(length)
        
        return strings_found

if __name__ == '__main__':
    filename = '/workspace/heapdump.hprof'
    strings = read_hprof(filename)
    print(f"\n\nFound {len(strings)} interesting strings")
    for s in strings:
        print(s)
