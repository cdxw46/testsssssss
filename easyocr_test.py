#!/usr/bin/env python3
import easyocr
import requests
import cv2
import numpy as np
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

# Inicializar reader (puede tardar un poco la primera vez)
print("Inicializando EasyOCR...")
reader = easyocr.Reader(['en'], gpu=False)
print("EasyOCR listo")

# Crear sesión
session = requests.Session()
session.get(BASE_URL)

# Descargar CAPTCHA
print("Descargando CAPTCHA...")
img_response = session.get(BASE_URL + "mturk.php")
img_array = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

# Preprocesar
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
resized = cv2.resize(binary, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

# OCR con EasyOCR
print("Haciendo OCR...")
result = reader.readtext(resized, allowlist='0123456789+=')

print("\nResultados de EasyOCR:")
for (bbox, text, conf) in result:
    print(f"  '{text}' (confianza: {conf:.2f})")

# Concatenar todo el texto detectado
full_text = ''.join([text for (_, text, _) in result])
print(f"\nTexto completo: '{full_text}'")

# Buscar números
numbers = re.findall(r'\d+', full_text)
print(f"Números encontrados: {numbers}")

if len(numbers) >= 2:
    a = int(numbers[0])
    b = int(numbers[1])
    result_calc = a + b
    print(f"\nCalculando: {a} + {b} = {result_calc}")
    
    # Enviar
    data = {"captcha": str(result_calc)}
    response = session.post(BASE_URL, data=data)
    
    # Ver resultado
    alerts = re.findall(r"alert[^>]*>([^<]+)</", response.text)
    if alerts:
        print(f"Respuesta del servidor: {alerts[0]}")
    
    if "flag" in response.text.lower() or "247ctf" in response.text.lower():
        print("\n" + "="*60)
        print(response.text[:1000])
