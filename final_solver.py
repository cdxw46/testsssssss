#!/usr/bin/env python3
import easyocr
import requests
import cv2
import numpy as np
import re
import time

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

# Inicializar reader
print("Inicializando EasyOCR...")
reader = easyocr.Reader(['en'], gpu=False, verbose=False)
print("EasyOCR listo\n")

def solve_captcha(session, reader):
    """Resuelve un CAPTCHA y devuelve si fue exitoso"""
    try:
        # Descargar CAPTCHA
        img_response = session.get(BASE_URL + "mturk.php")
        img_array = np.frombuffer(img_response.content, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        # Preprocesar
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        resized = cv2.resize(binary, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        
        # OCR
        result = reader.readtext(resized, allowlist='0123456789+=')
        full_text = ''.join([text for (_, text, _) in result])
        
        # Extraer números
        numbers = re.findall(r'\d+', full_text)
        
        if len(numbers) >= 2:
            a = int(numbers[0])
            b = int(numbers[1])
            answer = a + b
            
            # Enviar respuesta
            data = {"captcha": str(answer)}
            response = session.post(BASE_URL, data=data)
            
            return True, answer, response.text
        else:
            return False, None, "No se encontraron suficientes números"
    except Exception as e:
        return False, None, str(e)

# Crear sesión
session = requests.Session()
session.get(BASE_URL)
print("Sesión iniciada\n")

start_time = time.time()
solved = 0

for i in range(100):
    success, answer, response_text = solve_captcha(session, reader)
    
    if success:
        solved += 1
        
        # Verificar si hay flag
        if "flag" in response_text.lower() or "247ctf{" in response_text:
            print(f"\n{'='*60}")
            print(f"¡FLAG ENCONTRADA después de {solved} intentos!")
            print(f"{'='*60}")
            # Extraer la flag
            flag_match = re.search(r'247CTF\{[^}]+\}', response_text, re.IGNORECASE)
            if flag_match:
                print(f"\nFLAG: {flag_match.group(0)}")
            else:
                print(response_text[:2000])
            break
        
        # Verificar mensajes de error
        if "invalid" in response_text.lower():
            print(f"{i+1}. ✗ Respuesta {answer} incorrecta")
        elif "timeout" in response_text.lower() or "too slow" in response_text.lower():
            print(f"{i+1}. ⚠ Timeout/Too slow")
            break
        else:
            if (i+1) % 10 == 0:
                elapsed = time.time() - start_time
                print(f"{i+1}. ✓ {solved} resueltos en {elapsed:.1f}s (promedio: {elapsed/solved:.2f}s/captcha)")
    else:
        print(f"{i+1}. ✗ Error: {response_text}")

elapsed = time.time() - start_time
print(f"\nTotal: {solved}/100 en {elapsed:.1f}s")
