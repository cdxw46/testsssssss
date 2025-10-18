#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

img_response = session.get(BASE_URL + "mturk.php")
nparr = np.frombuffer(img_response.content, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

print("Probando thresholds con Tesseract:\n")

for thresh_val in [100, 110, 120, 127, 130, 140]:
    print(f"Threshold {thresh_val}:")
    
    # Normal
    _, binary = cv2.threshold(img, thresh_val, 255, cv2.THRESH_BINARY)
    resized = cv2.resize(binary, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)
    text = pytesseract.image_to_string(resized, config='--psm 7').strip()
    if text:
        print(f"  Normal: '{text[:60]}'")
    
    # Inverso
    _, binary_inv = cv2.threshold(img, thresh_val, 255, cv2.THRESH_BINARY_INV)
    resized_inv = cv2.resize(binary_inv, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)
    text_inv = pytesseract.image_to_string(resized_inv, config='--psm 7').strip()
    if text_inv:
        print(f"  Inverso: '{text_inv[:60]}'")
    
    if not text and not text_inv:
        print(f"  (sin resultados)")
    
    print()
