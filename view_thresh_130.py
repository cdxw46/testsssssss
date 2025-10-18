#!/usr/bin/env python3
from PIL import Image
import numpy as np

# El threshold 130 mostró texto, veamos esa imagen procesada
img = Image.open('/workspace/thresh_130.png')
arr = np.array(img)

print(f"Threshold 130 procesado: {arr.shape}\n")

# Mostrar en ASCII reducido (cada 4 píxeles)
print("Vista reducida (cada 4 píxeles):\n")

for y in range(0, arr.shape[0], 4):
    row = []
    for x in range(0, arr.shape[1], 4):
        if len(arr.shape) == 3:
            val = arr[y, x, 0]
        else:
            val = arr[y, x]
        
        row.append('█' if val < 128 else ' ')
    
    line = ''.join(row)
    if line.strip():
        print(line)
