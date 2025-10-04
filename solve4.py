#!/usr/bin/env python3
from Crypto.Util.number import *
import gmpy2

# Datos del output
N = 5981664384988507891478572449251897296717727847212579781448791472718547112403550208352320926002397616312181279859738938646168022481824206589739320298482728968548378237391009138243024910596491172979923991673446034011260330224409794208875199561844435663744993504673450898288161482849187018770655419007178851937895764901674192425054643548670616348302447202491340266057221307744866082461604674766259695903766772980842036324667567850124019171425634526227426965833985082234968255176231124754301435374519312001547854794352023852342682220352109083558778402466358598254431167382653831478713628185748237886560605604945010671417

cts = [4064195644006411160585797813860027634920635349984344191047587061586620848352019080467087592184982883284356841385019453458842500930190512793665886381102812026066865666098391973664302897278510995945377153937248437062600080527317980210967973971371047319247120004523147629534186514628527555180736833194525516718549330721987873868571634294877416190209288629499265010822332662061001208360467692613959936438519512705706688327846470352610192922218603268096313278741647626899523312431823527174576009143724850631439559205050395629961996905961682800070679793831568617438035643749072976096500278297683944583609092132808342160168, 3972397619896893471633226994966440180689669532336298201562465946694941720775869427764056001983618377003841446300122954561092878433908258359050016399257266833626893700179430172867058140215023211349613449750819959868861260714924524414967854467488908710563470522800186889553825417008118394349306170727982570843758792622898850338954039322560740348595654863475541846505121081201633770673996898756298398831948133434844321091554344145679504115839940880338238034227536355386474785852916335583794757849746186832609785626770517073108801492522816245458992502698143396049695921044554959802743742110180934416272358039695942552488, 956566266150449406104687131427865505474798294715598448065695308619216559681163085440476088324404921175885831054464222377255942505087330963629877648302727892001779224319839877897857215091085980519442914974498275528112936281916338633178398286676523416008365096599844169979821513770606168325175652094633129536643417367820830724397070621662683223203491074814734747601002376621653739871373924630026694962642922871008486127796621355314581093953946913681152270251669050414866366693593651789709229310574005739535880988490183275291507128529820194381392682870291338920077175831052974790596134745552552808640002791037755434586]

hint = 2674558878275613295915981392537201653631411909654166620884912623530781

print("[+] El hint parece contener parte de la flag!")
hint_bytes = long_to_bytes(hint)
print(f"[+] Hint: {hint_bytes}")
print(f"[+] Hint hex: {hint_bytes.hex()}")

# El hint empieza con "c4t|" que podría ser parte de "quickMaffs_c4t|..."
# o algo similar

# Intentemos el ataque de Hastad con e=3
# Para mensajes pequeños, si m^3 < N, entonces c = m^3
print("\n[*] Intentando ataque de Hastad con e=3...")

# Verificar cada cifrado
messages = []
for i, ct in enumerate(cts):
    # Intentar raíz cúbica
    m, is_exact = gmpy2.iroot(ct, 3)
    
    if is_exact:
        print(f"[!] Cifrado {i+1} es un cubo perfecto!")
        messages.append(int(m))
        msg_bytes = long_to_bytes(int(m))
        print(f"    Mensaje: {msg_bytes}")
        print(f"    Hex: {msg_bytes.hex()}")
    else:
        # Si no es exacto, intentar con múltiplos de N
        found = False
        for k in range(1, 20):
            c_adjusted = ct + k * N
            m2, is_exact2 = gmpy2.iroot(c_adjusted, 3)
            if is_exact2:
                print(f"[!] Cifrado {i+1} con k={k} es un cubo perfecto!")
                messages.append(int(m2))
                msg_bytes = long_to_bytes(int(m2))
                print(f"    Mensaje: {msg_bytes}")
                print(f"    Hex: {msg_bytes.hex()}")
                found = True
                break
        
        if not found:
            print(f"[-] No se pudo encontrar raíz cúbica exacta para cifrado {i+1}")

if len(messages) == len(cts):
    print(f"\n[+] Encontrados {len(messages)} mensajes")
    print(f"[+] Suma de los mensajes: {sum(messages)}")
    print(f"[+] Hint esperado: {hint}")
    
    if sum(messages) == hint:
        print("\n[!!!] LA SUMA COINCIDE! Los mensajes son correctos!")
        
        # Mostrar cada mensaje decodificado
        for i, m in enumerate(messages):
            msg = long_to_bytes(m)
            print(f"\n[+] Mensaje {i+1}:")
            print(f"    Decimal: {m}")
            print(f"    Hex: {msg.hex()}")
            print(f"    Texto: {msg}")
        
        # Buscar la flag en los mensajes
        all_messages = b''.join([long_to_bytes(m) for m in messages])
        print(f"\n[+] Todos los mensajes concatenados: {all_messages}")
        
        # La flag podría estar en uno de los mensajes o ser la concatenación
        for i, m in enumerate(messages):
            msg = long_to_bytes(m).decode('utf-8', errors='ignore')
            if 'HTB{' in msg or 'htb{' in msg:
                print(f"\n[!!!] FLAG ENCONTRADA en mensaje {i+1}: {msg}")

# Si e=3 no funciona, probar con otros exponentes pequeños
else:
    print("\n[*] e=3 no funcionó. Probando con otros exponentes...")
    
    for e in [5, 7, 11, 13, 17]:
        print(f"\n[*] Probando e={e}...")
        messages = []
        
        for i, ct in enumerate(cts):
            m, is_exact = gmpy2.iroot(ct, e)
            
            if is_exact:
                messages.append(int(m))
            else:
                # Probar con múltiplos de N
                found = False
                for k in range(1, 10):
                    c_adjusted = ct + k * N
                    m2, is_exact2 = gmpy2.iroot(c_adjusted, e)
                    if is_exact2:
                        messages.append(int(m2))
                        found = True
                        break
                
                if not found:
                    break
        
        if len(messages) == len(cts) and sum(messages) == hint:
            print(f"[!!!] ÉXITO con e={e}!")
            for i, m in enumerate(messages):
                msg = long_to_bytes(m)
                print(f"Mensaje {i+1}: {msg}")
            break