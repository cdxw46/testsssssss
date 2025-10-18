#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar CAPTCHA
img_response = session.get(BASE_URL + "mturk.php")
img_array = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Probar TODOS los thresholds y PSMs
print("Probando todas las combinaciones:\n")

best_candidates = []

for thresh_val in [90, 100, 110, 120, 130]:
    _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    resized = cv2.resize(binary, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    
    for psm in range(3, 14):
        try:
            text = pytesseract.image_to_string(resized, config=f'--psm {psm}').strip()
            
            # Buscar números
            numbers = re.findall(r'\d+', text)
            
            if len(numbers) >= 2:
                # Posible candidato
                best_candidates.append({
                    'thresh': thresh_val,
                    'psm': psm,
                    'text': text,
                    'numbers': numbers
                })
        except:
            pass

# Mostrar mejores candidatos
print(f"Encontrados {len(best_candidates)} candidatos con al menos 2 números:\n")

for candidate in best_candidates[:10]:  # Mostrar primeros 10
    print(f"Thresh {candidate['thresh']}, PSM {candidate['psm']}:")
    print(f"  Texto: '{candidate['text'][:80]}'")
    print(f"  Números: {candidate['numbers'][:5]}")
    
    if len(candidate['numbers']) >= 2:
        a = int(candidate['numbers'][0])
        b = int(candidate['numbers'][1])
        print(f"  Ecuación: {a} + {b} = {a+b}")
    print()
