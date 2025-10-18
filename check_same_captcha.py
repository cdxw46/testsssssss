#!/usr/bin/env python3
import requests
import hashlib

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar el mismo CAPTCHA 3 veces
hashes = []
for i in range(3):
    img_response = session.get(BASE_URL + "mturk.php")
    img_hash = hashlib.md5(img_response.content).hexdigest()
    hashes.append(img_hash)
    print(f"Descarga {i+1}: {img_hash} ({len(img_response.content)} bytes)")

if len(set(hashes)) == 1:
    print("\n✓ El mismo CAPTCHA se mantiene en la sesión")
else:
    print("\n✗ El CAPTCHA cambia en cada descarga")
