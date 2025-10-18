#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re
import time

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

# Crear sesión
session = requests.Session()
response = session.get(BASE_URL)
print(f"Sesión iniciada")

# Primer CAPTCHA
number_str = extract_number(session)
print(f"CAPTCHA 1: '{number_str}'")

if len(number_str) >= 6:
    # Probar división central
    mid = len(number_str) // 2
    num1 = number_str[:mid]
    num2 = number_str[mid:]
    
    a = int(num1)
    b = int(num2)
    result = a + b
    
    print(f"Enviando: {a} + {b} = {result}")
    data = {"captcha": str(result)}
    response = session.post(BASE_URL, data=data)
    
    print(f"\nContenido de la respuesta completa:")
    print(response.text[:1500])
    print("\n" + "="*60)
    
    # Intentar obtener segundo CAPTCHA
    print("\nIntentando obtener segundo CAPTCHA...")
    number_str2 = extract_number(session)
    print(f"CAPTCHA 2: '{number_str2}'")
    
    if number_str2 and number_str2 != number_str:
        print("✓ La sesión continúa, se obtuvo un nuevo CAPTCHA")
    else:
        print("✗ No se obtuvo un nuevo CAPTCHA o es el mismo")
