#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

# Crear sesión
session = requests.Session()
response = session.get(BASE_URL)

# Descargar CAPTCHA
img_response = session.get(BASE_URL + "mturk.php")
img_array = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

# Preprocesar
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Probar diferentes métodos de threshold
methods = [
    ("BINARY", cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]),
    ("OTSU", cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]),
    ("ADAPTIVE", cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)),
]

print("Probando diferentes métodos de preprocesamiento:\n")

for name, processed in methods:
    # Resize para mejor OCR
    resized = cv2.resize(processed, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    
    # Probar OCR
    custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789+='
    text = pytesseract.image_to_string(resized, config=custom_config)
    
    # También probar con datos detallados
    data = pytesseract.image_to_data(resized, output_type=pytesseract.Output.DICT, config='--psm 6')
    detected_text = ' '.join([str(data['text'][i]) for i in range(len(data['text'])) if int(data['conf'][i]) > 0])
    
    print(f"{name}:")
    print(f"  OCR normal: {text.strip()}")
    print(f"  OCR data: {detected_text}")
    print()

# Guardar imagen para inspección manual
cv2.imwrite('/workspace/debug_otsu.png', methods[1][1])
