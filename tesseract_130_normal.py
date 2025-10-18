#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re
import time

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

def solve_with_tess(session):
    try:
        session.get(BASE_URL)
        
        img_response = session.get(BASE_URL + "mturk.php")
        nparr = np.frombuffer(img_response.content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        # Threshold 130 NORMAL (no inverso), x10
        _, binary = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY)
        resized = cv2.resize(binary, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)
        
        # OCR
        text = pytesseract.image_to_string(resized, config='--psm 7').strip()
        
        # Extraer solo dígitos
        digits = re.sub(r'[^0-9]', '', text)
        
        if len(digits) >= 3:
            # Probar diferentes splits
            for split in range(1, min(len(digits), 10)):
                a = int(digits[:split])
                b = int(digits[split:])
                answer = a + b
                
                data = {"captcha": str(answer)}
                response = session.post(BASE_URL, data=data)
                
                if "invalid" not in response.text.lower():
                    return True, answer, response.text, split, digits
        
        return False, None, "No match", 0, digits
    except Exception as e:
        return False, None, str(e), 0, ""

# Probar con varios CAPTCHAs
print("Probando con threshold 130 normal:\n")

for i in range(10):
    session = requests.Session()
    
    success, answer, response_text, split, digits = solve_with_tess(session)
    
    if success:
        print(f"{i+1}. ✓✓✓ Dígitos: '{digits}', Split: {split}, Respuesta: {answer}")
        
        if "flag" in response_text.lower():
            flag_match = re.search(r'247CTF\{[^}]+\}', response_text, re.IGNORECASE)
            if flag_match:
                print(f"\n{flag_match.group(0)}")
                break
    else:
        print(f"{i+1}. ✗ Dígitos: '{digits}'")
