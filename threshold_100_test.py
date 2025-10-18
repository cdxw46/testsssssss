#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

def solve_with_threshold_100(session):
    # Descargar CAPTCHA
    img_response = session.get(BASE_URL + "mturk.php")
    img_array = np.frombuffer(img_response.content, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    resized = cv2.resize(binary, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    
    # Probar varias configuraciones
    texts = []
    for psm in [6, 7, 8, 11, 13]:
        text = pytesseract.image_to_string(resized, config=f'--psm {psm}').strip()
        texts.append((psm, text))
    
    return texts

# Probar con 5 CAPTCHAs
for i in range(5):
    print(f"\n{'='*60}")
    print(f"CAPTCHA #{i+1}")
    print(f"{'='*60}")
    
    session = requests.Session()
    session.get(BASE_URL)
    
    texts = solve_with_threshold_100(session)
    
    for psm, text in texts:
        if text and len(text) > 5:
            print(f"\nPSM {psm}: '{text}'")
            
            # Extraer todos los números
            numbers = re.findall(r'\d+', text)
            print(f"  Números: {numbers}")
            
            # Buscar patrones de suma
            # Patrón 1: NUM + NUM
            match = re.search(r'(\d+)\s*[\+\*x]\s*(\d+)', text)
            if match and len(numbers) >= 2:
                a = int(numbers[0])
                b = int(numbers[1])
                result = a + b
                
                print(f"  Probando: {a} + {b} = {result}")
                
                data = {"captcha": str(result)}
                response = session.post(BASE_URL, data=data)
                
                if "invalid" in response.text.lower():
                    print(f"  ✗ Incorrecto")
                elif "correct" in response.text.lower() or "invalid" not in response.text.lower():
                    print(f"  ✓✓✓ CORRECTO!")
                    if "flag" in response.text.lower() or "247ctf" in response.text.lower():
                        print("\n" + "="*60)
                        print("FLAG ENCONTRADA:")
                        print("="*60)
                        flag_match = re.search(r'247CTF\{[^}]+\}', response.text, re.IGNORECASE)
                        if flag_match:
                            print(flag_match.group(0))
                
                break  # Probar solo una vez por CAPTCHA
