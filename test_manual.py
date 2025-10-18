#!/usr/bin/env python3
import requests
import re

BASE_URL = "https://087ba594e710a16e.247ctf.com/"

# Probar respuestas aleatorias para ver el mensaje
session = requests.Session()
session.get(BASE_URL)

test_answers = ["1", "100", "1000", "12345", "999999", "0"]

for answer in test_answers:
    session2 = requests.Session()
    session2.get(BASE_URL)
    session2.get(BASE_URL + "mturk.php")
    
    data = {"captcha": answer}
    response = session2.post(BASE_URL, data=data)
    
    alerts = re.findall(r"alert[^>]*>([^<]+)</", response.text)
    print(f"Respuesta '{answer}': {alerts[0] if alerts else 'Sin mensaje'}")
