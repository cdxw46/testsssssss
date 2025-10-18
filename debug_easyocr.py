#!/usr/bin/env python3
import easyocr
import requests
import cv2
import numpy as np
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

reader = easyocr.Reader(['en'], gpu=False, verbose=False)

# Probar 3 CAPTCHAs para ver qué está detectando
for test_num in range(3):
    print(f"\n{'='*60}")
    print(f"Test #{test_num+1}")
    print(f"{'='*60}")
    
    session = requests.Session()
    session.get(BASE_URL)
    
    # Descargar CAPTCHA
    img_response = session.get(BASE_URL + "mturk.php")
    img_array = np.frombuffer(img_response.content, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    # Probar diferentes preprocesos
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    configs = [
        ("Threshold 120, x4", cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1], 4),
        ("Threshold 140, x4", cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)[1], 4),
        ("Otsu, x4", cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1], 4),
        ("Threshold 120, x5", cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1], 5),
    ]
    
    for name, processed, scale in configs:
        resized = cv2.resize(processed, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        
        # OCR
        result = reader.readtext(resized, allowlist='0123456789+=')
        full_text = ''.join([text for (_, text, _) in result])
        
        # Extraer números
        numbers = re.findall(r'\d+', full_text)
        
        if len(numbers) >= 2:
            a = int(numbers[0])
            b = int(numbers[1])
            answer = a + b
            
            print(f"\n{name}:")
            print(f"  Texto: '{full_text}'")
            print(f"  Ecuación: {a} + {b} = {answer}")
            
            # Probar esta respuesta
            session2 = requests.Session()
            session2.get(BASE_URL)
            session2.get(BASE_URL + "mturk.php")  # Mismo CAPTCHA
            
            data = {"captcha": str(answer)}
            response = session2.post(BASE_URL, data=data)
            
            if "invalid" in response.text.lower():
                print(f"  Resultado: ✗ Incorrecto")
            elif "correct" in response.text.lower():
                print(f"  Resultado: ✓ CORRECTO!")
            else:
                print(f"  Resultado: ? Sin mensaje claro")
