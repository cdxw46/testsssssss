#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar y guardar imagen
img_response = session.get(BASE_URL + "mturk.php")
with open('/workspace/debug_captcha.png', 'wb') as f:
    f.write(img_response.content)

print("Imagen guardada. Analizando...\n")

# Cargar imagen
img = cv2.imread('/workspace/debug_captcha.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Probar TODOS los thresholds posibles con x10
print("Probando todos los thresholds (inverso, x10):\n")

for thresh_val in range(110, 140, 5):
    _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
    resized = cv2.resize(binary, None, fx=10, fy=10, interpolation=cv2.INTER_CUBIC)
    
    # Guardar para inspección
    cv2.imwrite(f'/workspace/thresh_{thresh_val}.png', resized)
    
    # OCR con config específica
    text = pytesseract.image_to_string(resized, config='--psm 7').strip()
    
    # Limpiar agresivamente
    cleaned = ''.join(c for c in text if c.isdigit() or c in '+= ')
    
    print(f"Threshold {thresh_val}:")
    print(f"  Raw: '{text[:60]}'")
    print(f"  Cleaned: '{cleaned[:60]}'")
    
    # Intentar extraer ecuación
    match = re.search(r'(\d+)\s*\+\s*(\d+)', cleaned)
    if match:
        a = int(match.group(1))
        b = int(match.group(2))
        result = a + b
        print(f"  Ecuación: {a} + {b} = {result}")
    
    # También extraer solo números
    nums = re.findall(r'\d+', cleaned)
    if len(nums) >= 2:
        print(f"  Números extraídos: {nums[:3]}")
    
    print()
