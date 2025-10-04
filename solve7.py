#!/usr/bin/env python3
from Crypto.Util.number import *
import gmpy2

# Datos del output
N = 5981664384988507891478572449251897296717727847212579781448791472718547112403550208352320926002397616312181279859738938646168022481824206589739320298482728968548378237391009138243024910596491172979923991673446034011260330224409794208875199561844435663744993504673450898288161482849187018770655419007178851937895764901674192425054643548670616348302447202491340266057221307744866082461604674766259695903766772980842036324667567850124019171425634526227426965833985082234968255176231124754301435374519312001547854794352023852342682220352109083558778402466358598254431167382653831478713628185748237886560605604945010671417

cts = [4064195644006411160585797813860027634920635349984344191047587061586620848352019080467087592184982883284356841385019453458842500930190512793665886381102812026066865666098391973664302897278510995945377153937248437062600080527317980210967973971371047319247120004523147629534186514628527555180736833194525516718549330721987873868571634294877416190209288629499265010822332662061001208360467692613959936438519512705706688327846470352610192922218603268096313278741647626899523312431823527174576009143724850631439559205050395629961996905961682800070679793831568617438035643749072976096500278297683944583609092132808342160168, 3972397619896893471633226994966440180689669532336298201562465946694941720775869427764056001983618377003841446300122954561092878433908258359050016399257266833626893700179430172867058140215023211349613449750819959868861260714924524414967854467488908710563470522800186889553825417008118394349306170727982570843758792622898850338954039322560740348595654863475541846505121081201633770673996898756298398831948133434844321091554344145679504115839940880338238034227536355386474785852916335583794757849746186832609785626770517073108801492522816245458992502698143396049695921044554959802743742110180934416272358039695942552488, 956566266150449406104687131427865505474798294715598448065695308619216559681163085440476088324404921175885831054464222377255942505087330963629877648302727892001779224319839877897857215091085980519442914974498275528112936281916338633178398286676523416008365096599844169979821513770606168325175652094633129536643417367820830724397070621662683223203491074814734747601002376621653739871373924630026694962642922871008486127796621355314581093953946913681152270251669050414866366693593651789709229310574005739535880988490183275291507128529820194381392682870291338920077175831052974790596134745552552808640002791037755434586]

hint = 2674558878275613295915981392537201653631411909654166620884912623530781

print("[+] Analizando el problema desde una nueva perspectiva...")
print(f"[+] Hint (231 bits): {hint}")
print(f"[+] Hint como texto: {long_to_bytes(hint)}")

# Observación importante: el hint comienza con "c4t|"
# Esto sugiere que el hint mismo podría ser parte de la flag o contener información importante

# Voy a intentar un ataque diferente: Franklin-Reiter
# Si tenemos mensajes relacionados, podríamos recuperarlos

# Pero primero, intentemos algo más simple
# Si el hint es la suma de 4 mensajes y solo tenemos 3 cifrados,
# tal vez uno de los mensajes NO está cifrado

# Intentemos assumir que el 4to mensaje es conocido
# Por ejemplo, podría ser un mensaje estándar como "HTB{" o algo así

print("\n[*] Intentando con mensajes conocidos comunes...")

# Lista de posibles mensajes conocidos
known_messages = [
    b"HTB{",
    b"flag{",
    b"FLAG{",
    b"htb{",
    b"quick",
    b"maffs",
    b"quick_maffs",
    b"c4t"
]

# Agregar bytes individuales
known_messages += [bytes([i]) for i in range(256)]

for known in known_messages[:100]:  # Limitar para no tardar mucho
    if isinstance(known, bytes):
        m4 = bytes_to_long(known)
    else:
        continue
    
    # Si m1 + m2 + m3 + m4 = hint
    # Entonces m1 + m2 + m3 = hint - m4
    target_sum = hint - m4
    
    if target_sum <= 0:
        continue
    
    # Ahora necesitamos encontrar e tal que los 3 cifrados
    # descifrados sumen target_sum
    
    # Probar con exponentes pequeños
    for e in [3, 5, 7, 11, 13, 17, 19, 23]:
        # Para cada cifrado, calcular la raíz e-ésima
        roots = []
        all_found = True
        
        for ct in cts:
            # Intentar encontrar m tal que m^e ≡ ct (mod N)
            # Para mensajes pequeños, m^e podría ser < N o ligeramente mayor
            
            # Primero intentar raíz exacta
            root, is_exact = gmpy2.iroot(ct, e)
            if is_exact:
                roots.append(int(root))
            else:
                # Intentar con múltiplos de N
                found = False
                for k in range(1, 20):
                    test = ct + k * N
                    root2, is_exact2 = gmpy2.iroot(test, e)
                    if is_exact2:
                        roots.append(int(root2))
                        found = True
                        break
                
                if not found:
                    all_found = False
                    break
        
        if all_found and len(roots) == 3:
            if sum(roots) == target_sum:
                print(f"\n[!!!] ENCONTRADO con e={e} y 4to mensaje = {known}")
                print(f"[+] Mensajes:")
                all_messages = roots + [m4]
                for i, m in enumerate(all_messages):
                    msg = long_to_bytes(m)
                    print(f"    Mensaje {i+1}: {msg}")
                
                # Buscar la flag
                concatenated = b''.join([long_to_bytes(m) for m in all_messages])
                print(f"[+] Concatenados: {concatenated}")
                
                if b'HTB{' in concatenated:
                    flag_start = concatenated.index(b'HTB{')
                    flag_end = concatenated.index(b'}', flag_start) + 1
                    flag = concatenated[flag_start:flag_end]
                    print(f"\n[!!!] FLAG: {flag.decode()}")
                    exit(0)

# Si no encontramos con mensajes conocidos, intentemos otra cosa
print("\n[*] Intentando interpretar el hint de otra manera...")

# El hint podría ser la flag misma codificada de alguna manera
# Ya que empieza con "c4t|" que parece texto legible

# Intentemos decodificar el hint como diferentes encodings
hint_bytes = long_to_bytes(hint)
print(f"\n[+] Hint hex: {hint_bytes.hex()}")
print(f"[+] Hint ASCII (ignorando no imprimibles): ", end="")
for b in hint_bytes:
    if 32 <= b <= 126:
        print(chr(b), end="")
print()

# El patrón "c4t|" sugiere leet speak
# Podría ser parte de "cat" o algo similar

# Intentemos rotar/XOR el hint
print("\n[*] Intentando transformaciones simples del hint...")

# XOR con valores comunes
for key in [0x48, 0x54, 0x42]:  # H, T, B en ASCII
    xored = bytes([b ^ key for b in hint_bytes])
    if b'HTB' in xored or b'FLAG' in xored:
        print(f"[!] XOR con 0x{key:02x}: {xored}")

# Intentar rot13 o César
for shift in range(1, 26):
    shifted = []
    for b in hint_bytes:
        if ord('a') <= b <= ord('z'):
            shifted.append(chr((b - ord('a') + shift) % 26 + ord('a')))
        elif ord('A') <= b <= ord('Z'):
            shifted.append(chr((b - ord('A') + shift) % 26 + ord('A')))
        else:
            shifted.append(chr(b) if 32 <= b <= 126 else '?')
    shifted_str = ''.join(shifted)
    if 'HTB' in shifted_str or 'FLAG' in shifted_str:
        print(f"[!] ROT{shift}: {shifted_str}")

print("\n[*] El hint 'c4t|' podría ser leet speak...")
print("[+] Posibles interpretaciones:")
print("    c4t -> cat")
print("    Podría ser parte de 'quick_m4ffs_c4t' o similar")