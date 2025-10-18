#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re
import time

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

def extract_equation(img_bytes):
    """Intenta extraer la ecuación de la imagen"""
    img_array = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold binario
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Resize x4
    resized = cv2.resize(binary, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    
    # OCR con configuración para números
    text = pytesseract.image_to_string(resized, config='--psm 7').strip()
    
    # Extraer todos los números
    numbers = re.findall(r'\d+', text)
    
    return numbers, text

# Test inicial
session = requests.Session()
response = session.get(BASE_URL)
print(f"Sesión iniciada: {response.status_code}")

# Probar con una imagen
img_response = session.get(BASE_URL + "mturk.php")
numbers, full_text = extract_equation(img_response.content)

print(f"Texto detectado: '{full_text}'")
print(f"Números: {numbers}")

if len(numbers) >= 2:
    a = int(numbers[0])
    b = int(numbers[1])
    result = a + b
    print(f"Calculando: {a} + {b} = {result}")
    
    # Enviar
    data = {"captcha": str(result)}
    response = session.post(BASE_URL, data=data)
    
    # Ver respuesta
    if "flag" in response.text.lower() or "247ctf" in response.text.lower():
        print("\n" + "="*60)
        print("FLAG ENCONTRADA:")
        print("="*60)
        print(response.text)
    else:
        # Buscar mensajes de alert
        alerts = re.findall(r"alert[^>]*>([^<]+)</", response.text)
        for alert in alerts:
            print(f"Mensaje: {alert}")
        
        # Si pasamos el primer CAPTCHA, intentar resolver 100
        if "correct" in response.text.lower() or "session" not in response.text.lower():
            print("\n¡Primera respuesta correcta! Intentando resolver 100...")
            
            count = 1
            start = time.time()
            
            for i in range(99):
                try:
                    # Descargar nuevo CAPTCHA
                    img_response = session.get(BASE_URL + "mturk.php")
                    numbers, text = extract_equation(img_response.content)
                    
                    if len(numbers) >= 2:
                        result = int(numbers[0]) + int(numbers[1])
                        data = {"captcha": str(result)}
                        response = session.post(BASE_URL, data=data)
                        
                        if "flag" in response.text.lower() or "247ctf" in response.text.lower():
                            print("\n" + "="*60)
                            print("¡FLAG ENCONTRADA!")
                            print("="*60)
                            print(response.text)
                            break
                        
                        count += 1
                        if (i+1) % 10 == 0:
                            elapsed = time.time() - start
                            print(f"Progreso: {count}/100 en {elapsed:.1f}s")
                    else:
                        print(f"Fallo en iteración {i+2}: no se pudieron extraer números")
                except Exception as e:
                    print(f"Error en iteración {i+2}: {e}")
            
            elapsed = time.time() - start
            print(f"\nTotal: {count}/100 en {elapsed:.1f}s")
else:
    print("No se pudieron extraer suficientes números para calcular")
