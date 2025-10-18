#!/usr/bin/env python3
import requests
from PIL import Image
import io
import re
import pytesseract

# URL del desafío
BASE_URL = "https://087ba594e710a16e.247ctf.com/"

# Crear sesión
session = requests.Session()

# Hacer request inicial para obtener cookies
response = session.get(BASE_URL)
print(f"Sesión iniciada: {response.status_code}")

# Descargar imagen CAPTCHA
img_response = session.get(BASE_URL + "mturk.php")
img = Image.open(io.BytesIO(img_response.content))
img.save('/workspace/test_captcha.png')

# Preprocesar imagen - usar escala de grises con threshold normal
img_gray = img.convert('L')  # Convertir a escala de grises

# Threshold para convertir a blanco y negro (texto negro en fondo blanco)
threshold = 160
img_proc = img_gray.point(lambda p: 255 if p > threshold else 0)
img_proc = img_proc.resize((img.width * 4, img.height * 4), Image.LANCZOS)
img_proc.save('/workspace/test_captcha_proc.png')

# Hacer OCR con config optimizado para dígitos y símbolos
text = pytesseract.image_to_string(img_proc, config='--psm 7')
print(f"Texto detectado PSM7: '{text}'")

# Parsear números y operación
# Intentar encontrar patrón como "620925 + 44 = ?"
numbers = re.findall(r'\d+', text)
print(f"Números encontrados: {numbers}")

if len(numbers) >= 2:
    num1 = int(numbers[0])
    num2 = int(numbers[1])
    result = num1 + num2
    print(f"Resultado: {num1} + {num2} = {result}")
    
    # Enviar respuesta
    data = {"captcha": str(result)}
    response = session.post(BASE_URL, data=data)
    print(f"\nRespuesta del servidor:")
    print(response.text[:500])
