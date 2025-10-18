#!/usr/bin/env python3
import cv2
import numpy as np
import requests
from PIL import Image

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()
session.get(BASE_URL)

# Descargar imagen
img_response = session.get(BASE_URL + "mturk.php")
img = Image.open(io.BytesIO(img_response.content))

print(f"Tamaño: {img.size}")

# Convertir a modo RGB si no lo es
if img.mode != 'RGB':
    img = img.convert('RGB')

# Analizar histograma de colores
pixels = list(img.getdata())
unique_colors = set(pixels)
print(f"Colores únicos: {len(unique_colors)}")

# Mostrar algunos colores
for i, color in enumerate(list(unique_colors)[:20]):
    print(f"  Color {i}: RGB{color}")

# Verificar si hay texto en colores específicos
# El texto del CAPTCHA probablemente esté en un color oscuro
dark_pixels = [p for p in pixels if all(c < 150 for c in p)]
print(f"\nPíxeles oscuros (RGB < 150): {len(dark_pixels)} de {len(pixels)} ({100*len(dark_pixels)/len(pixels):.1f}%)")
