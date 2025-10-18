#!/usr/bin/env python3
import requests

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar y guardar CAPTCHA
img_response = session.get(BASE_URL + "mturk.php")

with open('/workspace/captcha_to_solve.png', 'wb') as f:
    f.write(img_response.content)

print("CAPTCHA guardado en /workspace/captcha_to_solve.png")
print(f"Tamaño: {len(img_response.content)} bytes")

# Ahora intentemos con múltiples configuraciones de Tesseract
import cv2
import numpy as np
import pytesseract

img = cv2.imread('/workspace/captcha_to_solve.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Probar inversión y diferentes escalas
configs = [
    (127, False, 10, '--psm 7'),
    (127, True, 10, '--psm 7'),
    (150, False, 10, '--psm 7'),
    (150, True, 10, '--psm 7'),
    (100, False, 10, '--psm 7'),
    (100, True, 10, '--psm 7'),
]

print("\nProbando configuraciones:")
for thresh_val, invert, scale, psm in configs:
    if invert:
        _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
    else:
        _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    
    resized = cv2.resize(binary, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    text = pytesseract.image_to_string(resized, config=psm).strip()
    
    if text:
        print(f"Thresh={thresh_val}, Inv={invert}, Scale={scale}: '{text}'")
