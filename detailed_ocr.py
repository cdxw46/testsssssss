#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import requests

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar imagen
img_response = session.get(BASE_URL + "mturk.php")
img_array = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Diferentes preprocesos
methods = [
    ("Simple 120", cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1]),
    ("Simple 140", cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)[1]),
    ("Otsu", cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]),
]

for name, processed in methods:
    resized = cv2.resize(processed, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    
    # OCR detallado
    data = pytesseract.image_to_data(resized, output_type=Output.DICT, config='--psm 6')
    
    print(f"\n{name}:")
    # Mostrar solo texto con confianza > 60
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:
            text = data['text'][i].strip()
            if text:
                print(f"  '{text}' (conf: {data['conf'][i]})")
    
    # También mostrar el texto completo
    full_text = pytesseract.image_to_string(resized, config='--psm 6 -c tessedit_char_whitelist=0123456789+=')
    print(f"  Texto completo: '{full_text.strip()}'")

# Guardar mejor versión
_, best = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
best_resized = cv2.resize(best, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
cv2.imwrite('/workspace/ultra_processed.png', best_resized)
