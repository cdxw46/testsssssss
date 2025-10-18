#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re

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

# Threshold binario simple
_, binary = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)

# Resize
resized = cv2.resize(binary, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

# Dividir imagen en 3 partes aproximadas
height, width = resized.shape
part1 = resized[:, :int(width*0.4)]  # Primer número
part2 = resized[:, int(width*0.4):int(width*0.6)]  # Operador
part3 = resized[:, int(width*0.6):]  # Segundo número

# OCR en cada parte
config_nums = r'--psm 7 -c tessedit_char_whitelist=0123456789'
config_ops = r'--psm 7 -c tessedit_char_whitelist=+-='

num1_text = pytesseract.image_to_string(part1, config=config_nums).strip()
op_text = pytesseract.image_to_string(part2, config=config_ops).strip()
num2_text = pytesseract.image_to_string(part3, config=config_nums).strip()

print(f"Parte 1 (número): '{num1_text}'")
print(f"Parte 2 (operador): '{op_text}'")
print(f"Parte 3 (número): '{num2_text}'")

# También probar OCR completo
full_text = pytesseract.image_to_string(resized, config='--psm 7').strip()
print(f"\nTexto completo: '{full_text}'")

# Extraer números
nums = re.findall(r'\d+', full_text)
print(f"Números encontrados: {nums}")

if len(nums) >= 2:
    try:
        a = int(nums[0])
        b = int(nums[1])
        result = a + b
        print(f"\nCalculando: {a} + {b} = {result}")
        
        # Enviar respuesta
        data = {"captcha": str(result)}
        response = session.post(BASE_URL, data=data)
        print(f"\nRespuesta del servidor:")
        # Buscar mensajes importantes
        if "flag" in response.text.lower() or "247ctf" in response.text.lower():
            print(response.text)
        elif "correct" in response.text.lower():
            print("¡Respuesta correcta!")
        elif "wrong" in response.text.lower() or "incorrect" in response.text.lower():
            print("Respuesta incorrecta")
        else:
            # Buscar alerts
            import re
            alerts = re.findall(r"alert[^>]*>([^<]+)</", response.text)
            if alerts:
                for alert in alerts:
                    print(f"Alert: {alert}")
            else:
                print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")
