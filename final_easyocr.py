#!/usr/bin/env python3
import easyocr
import cv2
import numpy as np
import requests
import re
import time

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

print("Inicializando EasyOCR...")
reader = easyocr.Reader(['en'], gpu=False, verbose=False)

def solve_one(session, reader):
    img_response = session.get(BASE_URL + "mturk.php")
    nparr = np.frombuffer(img_response.content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    # Threshold inverso
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Mega resize
    mega = cv2.resize(thresh, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)
    
    # EasyOCR
    result = reader.readtext(mega, allowlist='0123456789+=')
    
    # Concatenar texto
    text = ''.join([t for (_, t, _) in result])
    
    return text

# Iniciar sesión
session = requests.Session()
session.get(BASE_URL)

start_time = time.time()
solved = 0

for i in range(100):
    try:
        text = solve_one(session, reader)
        
        # Parsear
        match = re.search(r'(\d+)\+(\d+)', text)
        if match:
            a = int(match.group(1))
            b = int(match.group(2))
            answer = a + b
            
            data = {"captcha": str(answer)}
            response = session.post(BASE_URL, data=data)
            
            if "invalid" not in response.text.lower():
                solved += 1
                
                if "flag" in response.text.lower() or "247ctf{" in response.text.lower():
                    flag_match = re.search(r'247CTF\{[^}]+\}', response.text, re.IGNORECASE)
                    if flag_match:
                        print(flag_match.group(0))
                        break
                
                if solved % 10 == 0:
                    elapsed = time.time() - start_time
                    print(f"{solved}/100 en {elapsed:.1f}s")
            elif "timeout" in response.text.lower() or "slow" in response.text.lower():
                print(f"Timeout después de {solved} resueltos")
                break
    except:
        pass

elapsed = time.time() - start_time
print(f"Total: {solved}/100 en {elapsed:.1f}s")
