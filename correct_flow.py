#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re
import time

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

def solve_correct(session):
    """
    Flujo correcto:
    1. GET / para mostrar el formulario (esto carga la imagen en el navegador)
    2. Sin volver a descargar mturk.php por separado
    3. POST la respuesta
    
    PERO para hacer OCR necesito descargar la imagen... 
    
    La solución es: cuando hago GET /, el navegador descarga mturk.php automáticamente
    para mostrarla. Esa es la imagen que debo responder.
    
    Entonces el flujo es:
    1. GET / (el servidor genera y guarda un CAPTCHA en la sesión)
    2. GET mturk.php (obtengo la imagen del CAPTCHA de la sesión)
    3. OCR
    4. POST / con la respuesta (responde al CAPTCHA de la sesión)
    """
    
    # GET / primero - esto inicializa el CAPTCHA en la sesión del servidor
    html_response = session.get(BASE_URL)
    
    # Ahora descargar la imagen - debería ser la misma que se mostró en el HTML
    img_response = session.get(BASE_URL + "mturk.php")
    nparr = np.frombuffer(img_response.content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    # OCR
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    mega = cv2.resize(thresh, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)
    text = pytesseract.image_to_string(mega).strip()
    cleaned = re.sub(r'[^0-9+]', '', text)
    
    # Parsear
    match = re.search(r'(\d+)\+(\d+)', cleaned)
    if match:
        a = int(match.group(1))
        b = int(match.group(2))
        return a, b, a + b, text
    
    # Sin match, intentar con números
    nums = re.findall(r'\d+', cleaned)
    if len(nums) >= 2:
        a, b = int(nums[0]), int(nums[1])
        return a, b, a + b, text
    
    return None, None, None, text

# Test
session = requests.Session()

print("Test con flujo correcto:\n")

for i in range(5):
    a, b, result, text = solve_correct(session)
    
    if result:
        print(f"{i+1}. OCR: '{text[:50]}'")
        print(f"   Ecuación: {a} + {b} = {result}")
        
        # NO volver a hacer GET, usar la misma sesión
        data = {"captcha": str(result)}
        response = session.post(BASE_URL, data=data)
        
        if "invalid" not in response.text.lower():
            print(f"   ✓✓✓ CORRECTO!")
            if "flag" in response.text.lower() or "247ctf{" in response.text.lower():
                flag_match = re.search(r'247CTF\{[^}]+\}', response.text, re.IGNORECASE)
                if flag_match:
                    print(f"\n{flag_match.group(0)}")
                break
        else:
            print(f"   ✗ Incorrecto")
    else:
        print(f"{i+1}. No se pudo parsear: '{text[:50]}'")
    
    print()
