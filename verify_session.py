#!/usr/bin/env python3
import requests
import hashlib

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

# Test 1: ¿El CAPTCHA permanece en la sesión?
print("Test 1: Verificar si el CAPTCHA permanece en la sesión\n")

session = requests.Session()
session.get(BASE_URL)

# Descargar CAPTCHA
img1 = session.get(BASE_URL + "mturk.php").content
hash1 = hashlib.md5(img1).hexdigest()
print(f"Primera descarga: {hash1}")

# Descargar de nuevo
img2 = session.get(BASE_URL + "mturk.php").content
hash2 = hashlib.md5(img2).hexdigest()
print(f"Segunda descarga: {hash2}")

print(f"¿Son iguales? {hash1 == hash2}\n")

# Test 2: ¿Enviar una respuesta cambia el CAPTCHA?
print("Test 2: ¿Enviar respuesta cambia el CAPTCHA?\n")

session2 = requests.Session()
session2.get(BASE_URL)

img_before = session2.get(BASE_URL + "mturk.php").content
hash_before = hashlib.md5(img_before).hexdigest()
print(f"Antes de enviar: {hash_before}")

# Enviar respuesta incorrecta
data = {"captcha": "12345"}
response = session2.post(BASE_URL, data=data)
print(f"Respuesta: {'Invalid' if 'invalid' in response.text.lower() else 'Otro'}")

img_after = session2.get(BASE_URL + "mturk.php").content
hash_after = hashlib.md5(img_after).hexdigest()
print(f"Después de enviar: {hash_after}")

print(f"¿Son iguales? {hash_before == hash_after}")
