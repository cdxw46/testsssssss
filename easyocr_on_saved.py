#!/usr/bin/env python3
import easyocr
import cv2
import numpy as np

print("Inicializando EasyOCR...")
reader = easyocr.Reader(['en'], gpu=False, verbose=False)

# Probar EasyOCR en la imagen guardada con threshold 130
img = cv2.imread('/workspace/thresh_130.png', cv2.IMREAD_GRAYSCALE)

print("Haciendo OCR en threshold 130...")

# EasyOCR
result = reader.readtext(img, allowlist='0123456789+=')

print("\nResultados:")
for (bbox, text, conf) in result:
    print(f"  '{text}' (conf: {conf:.2f}) en posición {bbox[0]}")

# Texto completo
full_text = ''.join([text for (_, text, _) in result])
print(f"\nTexto completo: '{full_text}'")

# También ver qué detecta sin whitelist
result_full = reader.readtext(img)
print("\nSin whitelist:")
for (bbox, text, conf) in result_full:
    if conf > 0.3:
        print(f"  '{text}' (conf: {conf:.2f})")
