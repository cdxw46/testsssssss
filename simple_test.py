#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

print("Test simple de un CAPTCHA...\n")

session = requests.Session()

print("1. GET /...")
session.get(BASE_URL)

print("2. GET mturk.php...")
img_response = session.get(BASE_URL + "mturk.php")

print("3. Preprocesar...")
nparr = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
_, thresh = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY_INV)
mega = cv2.resize(thresh, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)

print("4. OCR...")
text = pytesseract.image_to_string(mega, config='--psm 7').strip()

print(f"5. Texto: '{text[:100]}'")

cleaned = re.sub(r'[^0-9+]', '', text)
print(f"6. Limpio: '{cleaned}'")

match = re.search(r'(\d+)\+(\d+)', cleaned)
if match:
    a = int(match.group(1))
    b = int(match.group(2))
    answer = a + b
    
    print(f"7. Ecuación: {a} + {b} = {answer}")
    
    print("8. POST respuesta...")
    data = {"captcha": str(answer)}
    response = session.post(BASE_URL, data=data)
    
    print(f"9. Status: {response.status_code}")
    
    if "invalid" in response.text.lower():
        print("✗ Incorrecto")
    elif "correct" in response.text.lower() or "flag" in response.text.lower():
        print("✓ Correcto!")
        if "flag" in response.text.lower():
            flag_match = re.search(r'247CTF\{[^}]+\}', response.text, re.IGNORECASE)
            if flag_match:
                print(f"\n{flag_match.group(0)}")
    else:
        print("? Sin mensaje claro")
else:
    print("No se encontró patrón")
