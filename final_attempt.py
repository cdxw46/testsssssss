#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re
import time

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

def extract_equation_v2(session):
    """Nueva versión de extracción"""
    img_response = session.get(BASE_URL + "mturk.php")
    img_array = np.frombuffer(img_response.content, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold adaptativo
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    # Resize
    resized = cv2.resize(binary, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)
    
    # OCR sin filtros
    text = pytesseract.image_to_string(resized, config='--psm 7').strip()
    
    return text

# Test
session = requests.Session()
session.get(BASE_URL)

for i in range(3):
    text = extract_equation_v2(session)
    print(f"Test {i+1}: '{text}'")
    
    # Extraer números
    nums = re.findall(r'\d+', text)
    print(f"  Números: {nums}")
    
    if len(nums) >= 2:
        result = int(nums[0]) + int(nums[1])
        print(f"  {nums[0]} + {nums[1]} = {result}")
        
        data = {"captcha": str(result)}
        response = session.post(BASE_URL, data=data)
        
        if "invalid" in response.text.lower():
            print(f"  ✗ Incorrecto\n")
        else:
            print(f"  ✓ CORRECTO!\n")
    else:
        print()
