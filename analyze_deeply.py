#!/usr/bin/env python3
import requests
import cv2
import numpy as np
import pytesseract
from PIL import Image
import io

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar imagen raw
img_response = session.get(BASE_URL + "mturk.php")
img = Image.open(io.BytesIO(img_response.content))

print(f"Imagen: {img.size}, {img.mode}")

# Guardar sin procesar
img.save('/workspace/captcha_raw.png')

# Convertir para OpenCV
img_cv = cv2.imread('/workspace/captcha_raw.png')
gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

# Probar MUCHOS thresholds diferentes
print("\nProbando thresholds:")
for thresh_val in range(100, 220, 20):
    _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    resized = cv2.resize(binary, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    
    # OCR con diferentes configuraciones
    configs = [
        '--psm 6',
        '--psm 7',
        '--psm 8',
        '--psm 11',
        '--psm 13',
    ]
    
    for config in configs:
        text = pytesseract.image_to_string(resized, config=config).strip()
        if text and len(text) > 3:
            print(f"Thresh {thresh_val}, {config}: '{text}'")

# También probar con inversión
print("\nCon inversión:")
for thresh_val in [100, 120, 140, 160]:
    _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
    resized = cv2.resize(binary, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    
    text = pytesseract.image_to_string(resized, config='--psm 6').strip()
    if text and len(text) > 3:
        print(f"Thresh {thresh_val} INV: '{text}'")
