#!/usr/bin/env python3

import socket
import time

def connect_to_server():
    host = "83.136.250.6"
    port = 54098
    
    try:
        # Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(30)  # 30 second timeout
        
        # Connect to server
        print(f"Connecting to {host}:{port}...")
        s.connect((host, port))
        
        # Receive initial data
        data = s.recv(4096).decode('utf-8')
        print("Received:")
        print(data)
        
        # Send the solution
        solution = "H:0;CX:0,1;CX:0,3;H:2;CX:2,4"
        print(f"Sending solution: {solution}")
        s.send((solution + "\n").encode('utf-8'))
        
        # Wait a bit for processing
        time.sleep(1)
        
        # Receive response
        response = s.recv(4096).decode('utf-8')
        print("Response:")
        print(response)
        
        # Try to receive more data if available
        try:
            more_data = s.recv(4096).decode('utf-8')
            if more_data:
                print("Additional response:")
                print(more_data)
        except:
            pass
        
        # Close connection
        s.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    connect_to_server()