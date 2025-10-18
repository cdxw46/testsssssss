#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar imagen
img_response = session.get(BASE_URL + "mturk.php")
img_array = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold 120
_, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
resized = cv2.resize(binary, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

# Probar con whitelist que incluya + y =
text_with_ops = pytesseract.image_to_string(resized, config='--psm 7 -c tessedit_char_whitelist=0123456789+=').strip()
text_only_nums = pytesseract.image_to_string(resized, config='--psm 7 -c tessedit_char_whitelist=0123456789').strip()

print(f"Con operadores: '{text_with_ops}'")
print(f"Solo números: '{text_only_nums}'")

# También probar sin whitelist
text_full = pytesseract.image_to_string(resized, config='--psm 7').strip()
print(f"Sin filtro: '{text_full}'")

# Intentar detectar el formato con espacios
text_spaces = pytesseract.image_to_string(resized, config='--psm 6').strip()
print(f"PSM 6: '{text_spaces}'")

# Buscar patrón N + N o N + N =
patterns = [
    r'(\d+)\s*\+\s*(\d+)',
    r'(\d+)\+(\d+)',
    r'(\d{1,7})\s*(\d{1,7})',
]

print("\nBuscando patrones:")
for pattern in patterns:
    match = re.search(pattern, text_with_ops + " " + text_full + " " + text_spaces)
    if match:
        print(f"  Patrón '{pattern}' encontrado: {match.groups()}")

# Probar todas las divisiones posibles del número
print(f"\nProbando todas las divisiones con el servidor:")
number_string = text_only_nums

for split_point in range(1, min(len(number_string), 10)):
    num1 = number_string[:split_point]
    num2 = number_string[split_point:]
    
    if num1.isdigit() and num2.isdigit() and len(num2) > 0:
        a = int(num1)
        b = int(num2)
        result = a + b
        
        # Enviar
        data = {"captcha": str(result)}
        response = session.post(BASE_URL, data=data)
        
        # Verificar respuesta
        if "invalid" not in response.text.lower():
            print(f"  ✓ {a} + {b} = {result} -> ¡Posible formato correcto!")
            alerts = re.findall(r"alert[^>]*>([^<]+)</", response.text)
            for alert in alerts:
                print(f"    Mensaje: {alert}")
            if "flag" in response.text.lower():
                print("="*60)
                print(response.text)
                print("="*60)
                break
        else:
            print(f"  ✗ {a} + {b} = {result}")
        
        # Pequeña pausa para no sobrecargar
        import time
        time.sleep(0.1)
