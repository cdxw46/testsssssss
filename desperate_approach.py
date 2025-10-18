#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

# Probar con UNA imagen todos los thresholds y scales posibles
session = requests.Session()
session.get(BASE_URL)

img_response = session.get(BASE_URL + "mturk.php")
nparr = np.frombuffer(img_response.content, np.uint8)
img_orig = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

print("Probando TODAS las combinaciones posibles:\n")

candidates = []

for thresh_val in range(80, 200, 10):
    for inv in [False, True]:
        for scale in [5, 8, 10, 12, 15]:
            try:
                if inv:
                    _, binary = cv2.threshold(img_orig, thresh_val, 255, cv2.THRESH_BINARY_INV)
                else:
                    _, binary = cv2.threshold(img_orig, thresh_val, 255, cv2.THRESH_BINARY)
                
                resized = cv2.resize(binary, (img_orig.shape[1]*scale, img_orig.shape[0]*scale), 
                                   interpolation=cv2.INTER_CUBIC)
                
                # Probar diferentes PSMs
                for psm in [6, 7, 11, 13]:
                    text = pytesseract.image_to_string(resized, config=f'--psm {psm}').strip()
                    
                    # Limpiar
                    cleaned = re.sub(r'[^0-9+]', '', text)
                    
                    # Buscar patrón
                    match = re.search(r'(\d+)\+(\d+)', cleaned)
                    if match:
                        a = int(match.group(1))
                        b = int(match.group(2))
                        candidates.append({
                            'thresh': thresh_val,
                            'inv': inv,
                            'scale': scale,
                            'psm': psm,
                            'a': a,
                            'b': b,
                            'result': a + b
                        })
            except:
                pass

print(f"Encontrados {len(candidates)} candidatos\n")

# Probar los primeros 20
for i, cand in enumerate(candidates[:20]):
    print(f"{i+1}. T={cand['thresh']}, Inv={cand['inv']}, Scale={cand['scale']}, PSM={cand['psm']}")
    print(f"   {cand['a']} + {cand['b']} = {cand['result']}")
    
    # Probar con el servidor
    session2 = requests.Session()
    session2.get(BASE_URL)
    session2.get(BASE_URL + "mturk.php")  # Mismo CAPTCHA
    
    data = {"captcha": str(cand['result'])}
    response = session2.post(BASE_URL, data=data)
    
    if "invalid" not in response.text.lower():
        print(f"   ✓✓✓ CORRECTO!!!")
        print(f"\nConfiguración ganadora:")
        print(f"  Threshold: {cand['thresh']}")
        print(f"  Inverso: {cand['inv']}")
        print(f"  Scale: {cand['scale']}")
        print(f"  PSM: {cand['psm']}")
        break
    else:
        print(f"   ✗ Incorrecto")
