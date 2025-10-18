#!/usr/bin/env python3
import cv2
import numpy as np
import requests
import pytesseract

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar imagen
img_response = session.get(BASE_URL + "mturk.php")
img_array = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

# Convertir a escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar threshold para obtener solo el texto
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Encontrar contornos
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(f"Encontrados {len(contours)} contornos")

# Filtrar contornos muy pequeños (ruido)
min_area = 10
valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]

print(f"Contornos válidos (área > {min_area}): {len(valid_contours)}")

# Ordenar contornos de izquierda a derecha
valid_contours = sorted(valid_contours, key=lambda c: cv2.boundingRect(c)[0])

# Extraer cada carácter individual
characters = []
for i, contour in enumerate(valid_contours):
    x, y, w, h = cv2.boundingRect(contour)
    
    # Extraer el carácter
    char_img = binary[y:y+h, x:x+w]
    
    # Resize para mejorar OCR
    char_img = cv2.resize(char_img, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    
    # OCR en el carácter individual
    text = pytesseract.image_to_string(char_img, config='--psm 10 -c tessedit_char_whitelist=0123456789+=').strip()
    
    if text:
        characters.append(text)
        print(f"Carácter {i}: '{text}' (pos {x}, tamaño {w}x{h})")

print(f"\nCaracteres detectados: {characters}")
print(f"Texto completo: {''.join(characters)}")
