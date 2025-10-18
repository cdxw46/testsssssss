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
img_array = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

print(f"Imagen original: {img.shape}")

# Convertir a escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Calcular histograma para encontrar mejor threshold
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
print(f"\nEstadísticas de píxeles:")
print(f"  Min: {gray.min()}, Max: {gray.max()}, Mean: {gray.mean():.1f}, Std: {gray.std():.1f}")

# Probar múltiples thresholds
thresholds = [120, 140, 160, 180, 200]

print("\nProbando diferentes thresholds:")
for thresh_val in thresholds:
    _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    resized = cv2.resize(binary, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    
    # OCR
    text1 = pytesseract.image_to_string(resized, config='--psm 6')
    text2 = pytesseract.image_to_string(resized, config='--psm 7')
    
    if text1.strip() or text2.strip():
        print(f"\nThreshold {thresh_val}:")
        print(f"  PSM6: '{text1.strip()}'")
        print(f"  PSM7: '{text2.strip()}'")

# Probar con inversión
print("\n\nProbando con imagen invertida:")
for thresh_val in [120, 140, 160]:
    _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
    resized = cv2.resize(binary, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    
    text = pytesseract.image_to_string(resized, config='--psm 6')
    if text.strip():
        print(f"Threshold {thresh_val} (INV): '{text.strip()}'")

# Probar con denoising
print("\n\nProbando con denoising:")
denoised = cv2.fastNlMeansDenoising(gray)
_, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
resized = cv2.resize(binary, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

text = pytesseract.image_to_string(resized, config='--psm 6')
print(f"Con denoising: '{text.strip()}'")

# Guardar para inspección
cv2.imwrite('/workspace/best_processed.png', resized)
