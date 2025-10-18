#!/usr/bin/env python3
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
response = session.get(BASE_URL)
print("Contenido inicial:")
print(response.text[:800])

# Ver qué cookies tenemos
print(f"\nCookies: {session.cookies}")

# Descargar CAPTCHA
img_response = session.get(BASE_URL + "mturk.php")
print(f"\nCAPTCHA downloaded: {len(img_response.content)} bytes")

# Intentar enviar respuesta
data = {"captcha": "12345"}
response = session.post(BASE_URL, data=data)

print(f"\nRespuesta POST status: {response.status_code}")
print(f"Longitud respuesta: {len(response.text)}")

# Buscar mensajes
alerts = re.findall(r"<div[^>]*alert[^>]*>([^<]+)</div>", response.text)
print(f"\nAlertas encontradas: {alerts}")

# Buscar cualquier texto que contenga "invalid", "correct", "flag", etc
keywords = ["invalid", "correct", "wrong", "flag", "timeout", "slow", "complete"]
for keyword in keywords:
    if keyword in response.text.lower():
        # Extraer contexto alrededor
        idx = response.text.lower().find(keyword)
        context = response.text[max(0, idx-100):min(len(response.text), idx+100)]
        print(f"\nEncontrado '{keyword}':")
        print(context)
