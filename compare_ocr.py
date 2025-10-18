#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import easyocr
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

print("Inicializando EasyOCR...")
reader = easyocr.Reader(['en'], gpu=False, verbose=False)

# Probar UNA imagen con ambos
session = requests.Session()
session.get(BASE_URL)

img_response = session.get(BASE_URL + "mturk.php")
nparr = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

# Preprocesar
_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
mega = cv2.resize(thresh, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)

# EasyOCR
print("\nEasyOCR:")
result_easy = reader.readtext(mega, allowlist='0123456789+=')
text_easy = ''.join([t for (_, t, _) in result_easy])
print(f"  Texto: '{text_easy}'")

match_easy = re.search(r'(\d+)\+(\d+)', text_easy)
if match_easy:
    a_easy = int(match_easy.group(1))
    b_easy = int(match_easy.group(2))
    result_easy_val = a_easy + b_easy
    print(f"  Ecuación: {a_easy} + {b_easy} = {result_easy_val}")
    
    # Probar esta respuesta
    data = {"captcha": str(result_easy_val)}
    response = session.post(BASE_URL, data=data)
    
    if "invalid" in response.text.lower():
        print(f"  ✗ EasyOCR INCORRECTO")
    else:
        print(f"  ✓✓✓ EasyOCR CORRECTO!")

# Tesseract con MUCHAS configuraciones
print("\nTesseract (probando configs):")

configs = [
    ('--psm 6', ''),
    ('--psm 7', ''),
    ('--psm 8', ''),
    ('--psm 6', '-c tessedit_char_whitelist=0123456789+='),
    ('--psm 7', '-c tessedit_char_whitelist=0123456789+='),
]

for config, extra in configs:
    full_config = f'{config} {extra}'
    text_tess = pytesseract.image_to_string(mega, config=full_config).strip()
    cleaned = re.sub(r'[^0123456789+]', '', text_tess)
    
    match_tess = re.search(r'(\d+)\+(\d+)', cleaned)
    if match_tess:
        a_tess = int(match_tess.group(1))
        b_tess = int(match_tess.group(2))
        result_tess = a_tess + b_tess
        
        print(f"  Config '{full_config[:30]}':")
        print(f"    Texto: '{cleaned[:50]}'")
        print(f"    Ecuación: {a_tess} + {b_tess} = {result_tess}")
        
        # Comparar con EasyOCR
        if match_easy and result_tess == result_easy_val:
            print(f"    ✓ Coincide con EasyOCR!")
        elif match_easy:
            print(f"    ✗ Diferente de EasyOCR ({result_easy_val})")
