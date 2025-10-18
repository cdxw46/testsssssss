#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
from PIL import Image
import io

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

# Crear sesión
session = requests.Session()
response = session.get(BASE_URL)
print(f"Sesión: {response.status_code}")

# Descargar CAPTCHA
img_response = session.get(BASE_URL + "mturk.php")
img_array = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

# Convertir a escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar threshold
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Invertir si es necesario (texto blanco en fondo negro)
if np.mean(thresh) > 127:
    thresh = 255 - thresh

# Dilatar un poco para conectar caracteres
kernel = np.ones((2,2), np.uint8)
thresh = cv2.dilate(thresh, kernel, iterations=1)

# Resize para mejor OCR
thresh = cv2.resize(thresh, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

# Guardar para inspección
cv2.imwrite('/workspace/opencv_processed.png', thresh)

# OCR con diferentes configuraciones
configs = [
    '--psm 6',
    '--psm 7',
    '--psm 11',
    '--psm 13',
    '--psm 6 -c tessedit_char_whitelist=0123456789+=',
]

print("\nProbando diferentes configuraciones OCR:")
for config in configs:
    text = pytesseract.image_to_string(thresh, config=config)
    print(f"{config}: '{text.strip()}'")
