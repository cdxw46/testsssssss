#!/usr/bin/env python3
from Crypto.Util.number import *
import gmpy2

# Datos del output
N = 5981664384988507891478572449251897296717727847212579781448791472718547112403550208352320926002397616312181279859738938646168022481824206589739320298482728968548378237391009138243024910596491172979923991673446034011260330224409794208875199561844435663744993504673450898288161482849187018770655419007178851937895764901674192425054643548670616348302447202491340266057221307744866082461604674766259695903766772980842036324667567850124019171425634526227426965833985082234968255176231124754301435374519312001547854794352023852342682220352109083558778402466358598254431167382653831478713628185748237886560605604945010671417

cts = [4064195644006411160585797813860027634920635349984344191047587061586620848352019080467087592184982883284356841385019453458842500930190512793665886381102812026066865666098391973664302897278510995945377153937248437062600080527317980210967973971371047319247120004523147629534186514628527555180736833194525516718549330721987873868571634294877416190209288629499265010822332662061001208360467692613959936438519512705706688327846470352610192922218603268096313278741647626899523312431823527174576009143724850631439559205050395629961996905961682800070679793831568617438035643749072976096500278297683944583609092132808342160168, 3972397619896893471633226994966440180689669532336298201562465946694941720775869427764056001983618377003841446300122954561092878433908258359050016399257266833626893700179430172867058140215023211349613449750819959868861260714924524414967854467488908710563470522800186889553825417008118394349306170727982570843758792622898850338954039322560740348595654863475541846505121081201633770673996898756298398831948133434844321091554344145679504115839940880338238034227536355386474785852916335583794757849746186832609785626770517073108801492522816245458992502698143396049695921044554959802743742110180934416272358039695942552488, 956566266150449406104687131427865505474798294715598448065695308619216559681163085440476088324404921175885831054464222377255942505087330963629877648302727892001779224319839877897857215091085980519442914974498275528112936281916338633178398286676523416008365096599844169979821513770606168325175652094633129536643417367820830724397070621662683223203491074814734747601002376621653739871373924630026694962642922871008486127796621355314581093953946913681152270251669050414866366693593651789709229310574005739535880988490183275291507128529820194381392682870291338920077175831052974790596134745552552808640002791037755434586]

hint = 2674558878275613295915981392537201653631411909654166620884912623530781

print("[+] Resolviendo quick_maffs...")
print(f"[+] N = {N} ({N.bit_length()} bits)")
print(f"[+] Tenemos {len(cts)} cifrados")
print(f"[+] Hint (suma) = {hint} ({hint.bit_length()} bits)")

# El hint es muy pequeño (231 bits) comparado con N (2046 bits)
# Esto significa que los mensajes son MUY pequeños

# Para mensajes tan pequeños, podemos usar el ataque de Hastad
# Si m < N^(1/e), entonces m^e < N y por lo tanto c = m^e (sin módulo)

# Pero ya verificamos que no son potencias perfectas simples
# Entonces necesitamos ser más creativos

# Una observación: el hint comienza con "c4t|"
hint_bytes = long_to_bytes(hint)
print(f"\n[+] Hint como bytes: {hint_bytes}")
print(f"[+] Hint hex: {hint_bytes.hex()}")

# Intentemos con el ataque de Coppersmith para mensajes pequeños
# Si los mensajes son de ~60-80 bits cada uno, entonces para e pequeño
# m^e podría ser solo ligeramente mayor que N

print("\n[*] Intentando ataque de Coppersmith/Hastad modificado...")

# Para cada posible e primo pequeño
for e in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]:
    # Para mensajes pequeños y e pequeño:
    # Si m es de ~77 bits (hint/3), entonces:
    # - Para e=3: m^3 es de ~231 bits
    # - Para e=5: m^5 es de ~385 bits
    # - Para e=7: m^7 es de ~539 bits
    
    # N es de 2046 bits, así que m^e << N para e pequeño
    
    # Esto significa que c = m^e mod N = m^e (sin módulo) si m es suficientemente pequeño
    # O c = m^e - k*N para algún k pequeño
    
    messages = []
    success = True
    
    for i, ct in enumerate(cts):
        found = False
        
        # Primero verificar si es una potencia perfecta
        m, is_exact = gmpy2.iroot(ct, e)
        if is_exact:
            messages.append(int(m))
            found = True
        else:
            # Si no es exacto, probar con múltiplos de N
            # Para mensajes pequeños, k debería ser 0
            # Pero podríamos tener c = m^e + k*N o c = m^e - k*N
            
            # Intentar c + k*N
            for k in range(1, 50):
                test = ct + k * N
                m2, is_exact2 = gmpy2.iroot(test, e)
                if is_exact2:
                    # Verificar que el mensaje sea razonable (pequeño)
                    if m2 < 2**100:  # Mensajes menores a 100 bits
                        messages.append(int(m2))
                        found = True
                        break
            
            if not found:
                # Intentar c - k*N (si c > k*N)
                for k in range(1, 10):
                    if ct > k * N:
                        test = ct - k * N
                        m3, is_exact3 = gmpy2.iroot(test, e)
                        if is_exact3 and m3 < 2**100:
                            messages.append(int(m3))
                            found = True
                            break
        
        if not found:
            success = False
            break
    
    if success and len(messages) == 3:
        # Verificar si la suma es correcta o cercana al hint
        total = sum(messages)
        
        # Podría haber un 4to mensaje o no
        if total == hint:
            print(f"\n[!!!] ÉXITO con e={e}! Suma exacta = hint")
            for i, m in enumerate(messages):
                msg = long_to_bytes(m)
                print(f"Mensaje {i+1}: {msg}")
                print(f"  Hex: {msg.hex()}")
            
            # Buscar la flag
            all_msg = b''.join([long_to_bytes(m) for m in messages])
            if b'HTB{' in all_msg:
                idx = all_msg.index(b'HTB{')
                flag_end = all_msg.index(b'}', idx) + 1
                print(f"\n[!!!] FLAG: {all_msg[idx:flag_end].decode()}")
                exit(0)
        elif total < hint:
            # Podría haber un 4to mensaje
            m4 = hint - total
            if m4 < 2**100:  # Verificar que sea razonable
                print(f"\n[!!!] ÉXITO con e={e}! 3 mensajes + 4to calculado")
                messages.append(m4)
                
                for i, m in enumerate(messages):
                    msg = long_to_bytes(m)
                    print(f"Mensaje {i+1}: {msg}")
                    print(f"  Hex: {msg.hex()}")
                
                # Buscar la flag
                all_msg = b''.join([long_to_bytes(m) for m in messages])
                if b'HTB{' in all_msg:
                    idx = all_msg.index(b'HTB{')
                    flag_end = all_msg.index(b'}', idx) + 1
                    print(f"\n[!!!] FLAG: {all_msg[idx:flag_end].decode()}")
                    exit(0)
                
                # También verificar si la flag está en mensajes individuales
                for m in messages:
                    msg = long_to_bytes(m).decode('utf-8', errors='ignore')
                    if 'HTB{' in msg:
                        print(f"\n[!!!] FLAG encontrada: {msg}")
                        exit(0)

# Si llegamos aquí, necesitamos otro enfoque
print("\n[*] Los ataques anteriores no funcionaron.")
print("[*] Analizando la estructura del hint más detalladamente...")

# El hint podría ser la flag misma
# "c4t|" podría ser parte de la flag en leet speak
# Por ejemplo: "quick_m4ffs_c4t" o algo similar

# Intentemos interpretarlo
hint_str = hint_bytes.decode('latin-1', errors='ignore')
print(f"\n[+] Hint decodificado: {repr(hint_str)}")

# Intentar encontrar patrones
if 'c4t' in hint_str:
    print("[+] El hint contiene 'c4t' que podría ser 'cat' en leet speak")

# El hint podría ser la concatenación directa de los mensajes
# o la flag podría estar escondida en el hint mismo