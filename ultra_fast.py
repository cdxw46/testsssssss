#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re
import time

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

def solve_fast(session):
    img_response = session.get(BASE_URL + "mturk.php")
    nparr = np.frombuffer(img_response.content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    # Threshold inverso
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Resize x10
    mega = cv2.resize(thresh, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)
    
    # OCR rápido
    text = pytesseract.image_to_string(mega).strip()
    
    # Limpiar
    cleaned = re.sub(r'[^0-9+\s]', '', text)
    
    return cleaned

# Iniciar
session = requests.Session()
session.get(BASE_URL)

start = time.time()
solved = 0

for i in range(100):
    try:
        text = solve_fast(session)
        
        # Buscar patrón
        match = re.search(r'(\d+)\s*\+\s*(\d+)', text)
        if not match:
            # Intentar con solo números
            nums = re.findall(r'\d+', text)
            if len(nums) >= 2:
                a, b = int(nums[0]), int(nums[1])
            else:
                continue
        else:
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
                print(f"{solved}/100 en {time.time()-start:.1f}s")
        elif "timeout" in response.text.lower() or "slow" in response.text.lower():
            print(f"Timeout en iteración {i+1}")
            break
    except:
        pass

print(f"Total: {solved}/100 en {time.time()-start:.1f}s")
