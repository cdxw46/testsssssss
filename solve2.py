#!/usr/bin/env python3
from Crypto.Util.number import *
import gmpy2
from itertools import combinations

# Datos del output
N = 5981664384988507891478572449251897296717727847212579781448791472718547112403550208352320926002397616312181279859738938646168022481824206589739320298482728968548378237391009138243024910596491172979923991673446034011260330224409794208875199561844435663744993504673450898288161482849187018770655419007178851937895764901674192425054643548670616348302447202491340266057221307744866082461604674766259695903766772980842036324667567850124019171425634526227426965833985082234968255176231124754301435374519312001547854794352023852342682220352109083558778402466358598254431167382653831478713628185748237886560605604945010671417

cts = [4064195644006411160585797813860027634920635349984344191047587061586620848352019080467087592184982883284356841385019453458842500930190512793665886381102812026066865666098391973664302897278510995945377153937248437062600080527317980210967973971371047319247120004523147629534186514628527555180736833194525516718549330721987873868571634294877416190209288629499265010822332662061001208360467692613959936438519512705706688327846470352610192922218603268096313278741647626899523312431823527174576009143724850631439559205050395629961996905961682800070679793831568617438035643749072976096500278297683944583609092132808342160168, 3972397619896893471633226994966440180689669532336298201562465946694941720775869427764056001983618377003841446300122954561092878433908258359050016399257266833626893700179430172867058140215023211349613449750819959868861260714924524414967854467488908710563470522800186889553825417008118394349306170727982570843758792622898850338954039322560740348595654863475541846505121081201633770673996898756298398831948133434844321091554344145679504115839940880338238034227536355386474785852916335583794757849746186832609785626770517073108801492522816245458992502698143396049695921044554959802743742110180934416272358039695942552488, 956566266150449406104687131427865505474798294715598448065695308619216559681163085440476088324404921175885831054464222377255942505087330963629877648302727892001779224319839877897857215091085980519442914974498275528112936281916338633178398286676523416008365096599844169979821513770606168325175652094633129536643417367820830724397070621662683223203491074814734747601002376621653739871373924630026694962642922871008486127796621355314581093953946913681152270251669050414866366693593651789709229310574005739535880988490183275291507128529820194381392682870291338920077175831052974790596134745552552808640002791037755434586]

hint = 2674558878275613295915981392537201653631411909654166620884912623530781

print("[+] Intentando ataque de exponente bajo con múltiples mensajes...")

# Generar lista de primos < 1024
primes = [i for i in range(2, 1024) if gmpy2.is_prime(i)]

# Para mensajes pequeños, si m^e < N, entonces c = m^e (sin módulo)
# Esto es especialmente probable para e pequeño

for e in primes[:50]:  # Probar primero los exponentes más pequeños
    # Intentar calcular la raíz e-ésima de cada cifrado
    ms = []
    all_exact = True
    
    for c in cts:
        m, exact = gmpy2.iroot(c, e)
        if exact:
            ms.append(m)
        else:
            all_exact = False
            break
    
    if all_exact and len(ms) == len(cts):
        # Verificar si la suma coincide con el hint
        if sum(ms) == hint:
            print(f"\n[!] ÉXITO! Encontrados todos los mensajes con e={e}")
            print(f"[+] La suma de los mensajes coincide: {sum(ms)} == {hint}")
            
            # Mostrar cada mensaje
            for i, m in enumerate(ms):
                print(f"\n[+] Mensaje {i+1}: {m}")
                msg_bytes = long_to_bytes(m)
                print(f"[+] Bytes hex: {msg_bytes.hex()}")
                
                # Intentar decodificar como texto
                try:
                    decoded = msg_bytes.decode('utf-8', errors='ignore')
                    print(f"[+] Decodificado UTF-8: {decoded}")
                except:
                    pass
                
                try:
                    decoded = msg_bytes.decode('latin-1', errors='ignore')
                    print(f"[+] Decodificado Latin-1: {decoded}")
                except:
                    pass
                
                # Buscar patrones de flag
                if b'HTB{' in msg_bytes or b'htb{' in msg_bytes or b'flag{' in msg_bytes:
                    print(f"\n[!!!] FLAG ENCONTRADA en mensaje {i+1}!")
                    
            # Concatenar todos los mensajes por si la flag está dividida
            all_messages = b''.join([long_to_bytes(m) for m in ms])
            print(f"\n[+] Todos los mensajes concatenados (hex): {all_messages.hex()}")
            try:
                print(f"[+] Decodificado: {all_messages.decode('utf-8', errors='ignore')}")
            except:
                pass
            
            break

# Si no encontramos con raíces exactas, intentar otro enfoque
else:
    print("\n[*] No se encontraron raíces exactas. Intentando enfoque diferente...")
    
    # Tal vez los mensajes son partes de una flag más grande
    # O necesitamos un ataque más sofisticado
    
    print("[*] Analizando estructura de los cifrados...")
    for i, c in enumerate(cts):
        print(f"[+] Cifrado {i+1}: {c.bit_length()} bits")
    
    print(f"\n[+] Hint (suma): {hint.bit_length()} bits")
    print(f"[+] Hint como bytes: {long_to_bytes(hint).hex()}")
    
    # Intentar con exponentes muy pequeños
    print("\n[*] Probando exponentes muy pequeños (3, 5, 7)...")
    for e in [3, 5, 7]:
        print(f"\n[*] Probando e = {e}")
        ms = []
        for i, c in enumerate(cts):
            # Intentar aproximación
            m_approx = int(c ** (1/e))
            
            # Probar valores cercanos
            for delta in range(-100, 101):
                m_test = m_approx + delta
                if pow(m_test, e, N) == c:
                    print(f"[!] Encontrado m{i+1} = {m_test}")
                    ms.append(m_test)
                    break
                # También probar sin módulo para mensajes pequeños
                if m_test ** e == c:
                    print(f"[!] Encontrado m{i+1} = {m_test} (sin módulo)")
                    ms.append(m_test)
                    break
        
        if len(ms) == len(cts):
            if sum(ms) == hint:
                print(f"\n[!] ÉXITO con e = {e}!")
                for i, m in enumerate(ms):
                    msg = long_to_bytes(m)
                    print(f"Mensaje {i+1}: {msg}")