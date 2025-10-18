#!/usr/bin/env python3
import easyocr
import cv2
import numpy as np
import requests
import re
import time

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

print("Inicializando EasyOCR...")
reader = easyocr.Reader(['en'], gpu=False, verbose=False)

def solve_fresh():
    """
    Flujo correcto completo:
    1. Crear sesión nueva
    2. GET / para inicializar
    3. GET mturk.php para obtener imagen (sin volver a hacer GET /)
    4. OCR
    5. POST respuesta en la MISMA sesión
    """
    
    session = requests.Session()
    
    # Paso 1: GET / para inicializar sesión
    session.get(BASE_URL)
    
    # Paso 2: GET mturk.php - esto obtiene el CAPTCHA de la sesión
    img_response = session.get(BASE_URL + "mturk.php")
    nparr = np.frombuffer(img_response.content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    # Paso 3: Preprocesar
    _, thresh = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY_INV)
    mega = cv2.resize(thresh, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)
    
    # Paso 4: OCR
    result = reader.readtext(mega, allowlist='0123456789+=')
    
    # Ordenar por posición X
    sorted_result = sorted(result, key=lambda x: x[0][0][0])
    ordered_text = ''.join([text for (_, text, _) in sorted_result])
    
    # Extraer números
    numbers_only = re.sub(r'[^0-9]', '', ordered_text)
    
    # Buscar símbolo +
    has_plus = '+' in ordered_text
    
    return session, numbers_only, ordered_text, has_plus

# Probar con 3 CAPTCHAs frescos
print("\nProbando con CAPTCHAs frescos:\n")

for test_num in range(3):
    print(f"Test {test_num+1}:")
    
    session, numbers, full_text, has_plus = solve_fresh()
    
    print(f"  Texto completo: '{full_text}'")
    print(f"  Solo números: '{numbers}'")
    print(f"  Tiene '+': {has_plus}")
    
    if len(numbers) >= 3:
        # Probar split en la mitad
        mid = len(numbers) // 2
        
        for offset in [0, -1, 1, -2, 2]:
            split = mid + offset
            if 0 < split < len(numbers):
                a = int(numbers[:split])
                b = int(numbers[split:])
                result = a + b
                
                data = {"captcha": str(result)}
                response = session.post(BASE_URL, data=data)
                
                if "invalid" not in response.text.lower():
                    print(f"  ✓✓✓ División {split}: {a} + {b} = {result}")
                    
                    if "flag" in response.text.lower():
                        flag_match = re.search(r'247CTF\{[^}]+\}', response.text, re.IGNORECASE)
                        if flag_match:
                            print(f"\n{flag_match.group(0)}")
                    break
    
    print()
