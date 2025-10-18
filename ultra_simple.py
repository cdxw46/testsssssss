#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar CAPTCHA
img_response = session.get(BASE_URL + "mturk.php")
nparr = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

# Inv threshold
_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

# Mega resize
mega = cv2.resize(thresh, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)

# Guardar
cv2.imwrite('/workspace/mega.png', mega)

# OCR ultra simple
text = pytesseract.image_to_string(mega)
print(f"Texto: '{text}'")

# También probar con Image
from PIL import Image
import io

img_pil = Image.open(io.BytesIO(img_response.content))
print(f"\nImagen PIL: {img_pil.size}, {img_pil.mode}")

# OCR directo
text2 = pytesseract.image_to_string(img_pil)
print(f"Texto directo: '{text2}'")

# Con resize
img_big = img_pil.resize((img_pil.width*10, img_pil.height*10), Image.LANCZOS)
text3 = pytesseract.image_to_string(img_big)
print(f"Texto x10: '{text3}'")
