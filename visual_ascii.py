#!/usr/bin/env python3
from PIL import Image
import numpy as np

img = Image.open('/workspace/captcha_to_solve.png')
arr = np.array(img)

print(f"Imagen: {arr.shape}\n")

# Convertir a ASCII art para visualizar
print("Vista ASCII de la imagen completa:\n")

for y in range(arr.shape[0]):
    row = []
    for x in range(arr.shape[1]):
        r, g, b = arr[y, x]
        intensity = (int(r) + int(g) + int(b)) // 3
        
        if intensity < 100:
            row.append('█')
        elif intensity < 150:
            row.append('▓')
        elif intensity < 200:
            row.append('▒')
        else:
            row.append(' ')
    
    print(''.join(row))
