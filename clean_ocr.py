#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

def extract_clean(session):
    img_response = session.get(BASE_URL + "mturk.php")
    nparr = np.frombuffer(img_response.content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    # Threshold inverso
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Mega resize
    mega = cv2.resize(thresh, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)
    
    # OCR
    text = pytesseract.image_to_string(mega).strip()
    
    # Limpiar: solo mantener dígitos, +, y espacios
    cleaned = re.sub(r'[^0-9+\s]', '', text)
    cleaned = ' '.join(cleaned.split())  # Normalizar espacios
    
    return text, cleaned

# Test con múltiples CAPTCHAs
print("Probando extracción limpia:\n")

for i in range(5):
    session = requests.Session()
    session.get(BASE_URL)
    
    raw, cleaned = extract_clean(session)
    
    print(f"CAPTCHA {i+1}:")
    print(f"  Raw: '{raw}'")
    print(f"  Cleaned: '{cleaned}'")
    
    # Buscar patrón NUM + NUM
    match = re.search(r'(\d+)\s*\+\s*(\d+)', cleaned)
    if match:
        a = int(match.group(1))
        b = int(match.group(2))
        result = a + b
        
        print(f"  Ecuación: {a} + {b} = {result}")
        
        # Probar
        data = {"captcha": str(result)}
        response = session.post(BASE_URL, data=data)
        
        if "invalid" in response.text.lower():
            print(f"  ✗ Incorrecto")
        else:
            print(f"  ✓✓✓ CORRECTO!")
            if "flag" in response.text.lower() or "247ctf{" in response.text.lower():
                print("\n" + "="*60)
                flag_match = re.search(r'247CTF\{[^}]+\}', response.text, re.IGNORECASE)
                if flag_match:
                    print(flag_match.group(0))
                else:
                    print(response.text[:1000])
    else:
        # Probar solo con números
        numbers = re.findall(r'\d+', cleaned)
        if len(numbers) >= 2:
            a = int(numbers[0])
            b = int(numbers[1])
            result = a + b
            print(f"  Números: {numbers[:2]} -> {a} + {b} = {result}")
            
            data = {"captcha": str(result)}
            response = session.post(BASE_URL, data=data)
            
            if "invalid" in response.text.lower():
                print(f"  ✗ Incorrecto")
            else:
                print(f"  ✓✓✓ CORRECTO!")
    
    print()
