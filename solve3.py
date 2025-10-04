#!/usr/bin/env python3
from Crypto.Util.number import *
import gmpy2

# Datos del output
N = 5981664384988507891478572449251897296717727847212579781448791472718547112403550208352320926002397616312181279859738938646168022481824206589739320298482728968548378237391009138243024910596491172979923991673446034011260330224409794208875199561844435663744993504673450898288161482849187018770655419007178851937895764901674192425054643548670616348302447202491340266057221307744866082461604674766259695903766772980842036324667567850124019171425634526227426965833985082234968255176231124754301435374519312001547854794352023852342682220352109083558778402466358598254431167382653831478713628185748237886560605604945010671417

cts = [4064195644006411160585797813860027634920635349984344191047587061586620848352019080467087592184982883284356841385019453458842500930190512793665886381102812026066865666098391973664302897278510995945377153937248437062600080527317980210967973971371047319247120004523147629534186514628527555180736833194525516718549330721987873868571634294877416190209288629499265010822332662061001208360467692613959936438519512705706688327846470352610192922218603268096313278741647626899523312431823527174576009143724850631439559205050395629961996905961682800070679793831568617438035643749072976096500278297683944583609092132808342160168, 3972397619896893471633226994966440180689669532336298201562465946694941720775869427764056001983618377003841446300122954561092878433908258359050016399257266833626893700179430172867058140215023211349613449750819959868861260714924524414967854467488908710563470522800186889553825417008118394349306170727982570843758792622898850338954039322560740348595654863475541846505121081201633770673996898756298398831948133434844321091554344145679504115839940880338238034227536355386474785852916335583794757849746186832609785626770517073108801492522816245458992502698143396049695921044554959802743742110180934416272358039695942552488, 956566266150449406104687131427865505474798294715598448065695308619216559681163085440476088324404921175885831054464222377255942505087330963629877648302727892001779224319839877897857215091085980519442914974498275528112936281916338633178398286676523416008365096599844169979821513770606168325175652094633129536643417367820830724397070621662683223203491074814734747601002376621653739871373924630026694962642922871008486127796621355314581093953946913681152270251669050414866366693593651789709229310574005739535880988490183275291507128529820194381392682870291338920077175831052974790596134745552552808640002791037755434586]

hint = 2674558878275613295915981392537201653631411909654166620884912623530781

print("[+] Analizando el hint más detalladamente...")
hint_bytes = long_to_bytes(hint)
print(f"[+] Hint como bytes hex: {hint_bytes.hex()}")
print(f"[+] Hint como texto: {hint_bytes}")
print(f"[+] Longitud del hint en bytes: {len(hint_bytes)}")

# El hint parece contener parte de la flag!
# 6334747c1ad62222dac3d70848dfc45c33370926084a37000a03eb331d
# Los primeros bytes parecen ser ASCII

# Intentar decodificar partes del hint
try:
    # Los primeros 4 bytes parecen ser "c4t|"
    print(f"\n[+] Primeros 8 bytes del hint: {hint_bytes[:8].hex()}")
    print(f"[+] Como texto: {hint_bytes[:8]}")
except:
    pass

# Ahora sabemos que los mensajes suman el hint
# Y el hint contiene información relacionada con la flag

print("\n[+] Buscando mensajes que sumen al hint...")

# Para e pequeño, es común que los mensajes sean pequeños
# Si m^e < N, entonces c = m^e (sin módulo)

# Verificar si los cifrados son potencias perfectas
for e in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
    all_roots = []
    all_exact = True
    
    for i, c in enumerate(cts):
        root, is_exact = gmpy2.iroot(c, e)
        if is_exact:
            all_roots.append(int(root))
        else:
            all_exact = False
            break
    
    if all_exact:
        total = sum(all_roots)
        print(f"\n[!] Encontradas raíces exactas para e={e}")
        print(f"[+] Suma de las raíces: {total}")
        print(f"[+] Hint esperado: {hint}")
        
        if total == hint:
            print(f"\n[!!!] ÉXITO! Los mensajes son:")
            for i, m in enumerate(all_roots):
                msg_bytes = long_to_bytes(m)
                print(f"[+] Mensaje {i+1}: {msg_bytes.hex()}")
                print(f"    Como texto: {msg_bytes}")
            
            # Concatenar todos los mensajes
            all_msg = b''.join([long_to_bytes(m) for m in all_roots])
            print(f"\n[+] Todos concatenados: {all_msg}")
            break

# Si no encontramos raíces exactas, intentar otra estrategia
# El hint podría ser la suma de los mensajes en texto plano

# Analicemos más el hint
print("\n[*] Analizando estructura del hint...")
print(f"[+] Hint en decimal: {hint}")

# Convertir a texto y buscar patrones
hint_str = long_to_bytes(hint)
print(f"[+] Hint como bytes: {hint_str}")

# Parece que el hint podría contener partes de la flag
# Intentemos decodificar byte por byte
print("\n[+] Decodificando hint byte por byte:")
for i, b in enumerate(hint_str):
    if 32 <= b <= 126:  # Caracteres imprimibles ASCII
        print(f"  Byte {i}: 0x{b:02x} = '{chr(b)}'")
    else:
        print(f"  Byte {i}: 0x{b:02x}")

# Ahora intentemos con exponentes pequeños específicos
# y verificar si la suma da el hint
print("\n[*] Probando con exponente 3 (el más común en RSA débil)...")

# Para e=3, verificar si los cifrados son cubos perfectos
roots = []
for i, c in enumerate(cts):
    root, is_exact = gmpy2.iroot(c, 3)
    if is_exact:
        print(f"[!] Cifrado {i+1} es un cubo perfecto!")
        print(f"    Raíz cúbica: {root}")
        roots.append(int(root))
        msg = long_to_bytes(int(root))
        print(f"    Como bytes: {msg.hex()}")
        print(f"    Como texto: {msg}")
    else:
        # Si no es exacto, podría estar ligeramente por encima de N
        # Intentar con múltiplos de N
        for k in range(1, 10):
            c_adjusted = c + k * N
            root2, is_exact2 = gmpy2.iroot(c_adjusted, 3)
            if is_exact2:
                print(f"[!] Cifrado {i+1} + {k}*N es un cubo perfecto!")
                roots.append(int(root2))
                msg = long_to_bytes(int(root2))
                print(f"    Como texto: {msg}")
                break

if len(roots) == len(cts):
    print(f"\n[+] Suma de los mensajes encontrados: {sum(roots)}")
    print(f"[+] Hint esperado: {hint}")
    if sum(roots) == hint:
        print("[!!!] La suma coincide! Flag encontrada!")