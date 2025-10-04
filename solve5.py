#!/usr/bin/env python3
from Crypto.Util.number import *
import gmpy2

# Datos del output
N = 5981664384988507891478572449251897296717727847212579781448791472718547112403550208352320926002397616312181279859738938646168022481824206589739320298482728968548378237391009138243024910596491172979923991673446034011260330224409794208875199561844435663744993504673450898288161482849187018770655419007178851937895764901674192425054643548670616348302447202491340266057221307744866082461604674766259695903766772980842036324667567850124019171425634526227426965833985082234968255176231124754301435374519312001547854794352023852342682220352109083558778402466358598254431167382653831478713628185748237886560605604945010671417

cts = [4064195644006411160585797813860027634920635349984344191047587061586620848352019080467087592184982883284356841385019453458842500930190512793665886381102812026066865666098391973664302897278510995945377153937248437062600080527317980210967973971371047319247120004523147629534186514628527555180736833194525516718549330721987873868571634294877416190209288629499265010822332662061001208360467692613959936438519512705706688327846470352610192922218603268096313278741647626899523312431823527174576009143724850631439559205050395629961996905961682800070679793831568617438035643749072976096500278297683944583609092132808342160168, 3972397619896893471633226994966440180689669532336298201562465946694941720775869427764056001983618377003841446300122954561092878433908258359050016399257266833626893700179430172867058140215023211349613449750819959868861260714924524414967854467488908710563470522800186889553825417008118394349306170727982570843758792622898850338954039322560740348595654863475541846505121081201633770673996898756298398831948133434844321091554344145679504115839940880338238034227536355386474785852916335583794757849746186832609785626770517073108801492522816245458992502698143396049695921044554959802743742110180934416272358039695942552488, 956566266150449406104687131427865505474798294715598448065695308619216559681163085440476088324404921175885831054464222377255942505087330963629877648302727892001779224319839877897857215091085980519442914974498275528112936281916338633178398286676523416008365096599844169979821513770606168325175652094633129536643417367820830724397070621662683223203491074814734747601002376621653739871373924630026694962642922871008486127796621355314581093953946913681152270251669050414866366693593651789709229310574005739535880988490183275291507128529820194381392682870291338920077175831052974790596134745552552808640002791037755434586]

hint = 2674558878275613295915981392537201653631411909654166620884912623530781

# IMPORTANTE: El código dice que hay 4 mensajes pero solo tenemos 3 cifrados en el output
# Esto podría ser un error o el 4to mensaje podría estar oculto

print("[+] Observación clave: El código menciona 4 puntos pero solo hay 3 cifrados!")
print(f"[+] Número de cifrados: {len(cts)}")
print(f"[+] Hint (suma de todos los pts): {hint}")
print(f"[+] Hint como texto: {long_to_bytes(hint)}")

# El hint comienza con "c4t|" que podría ser parte de la flag
# Analicemos si el 4to mensaje podría ser parte del hint

# Si tenemos 3 cifrados y el hint es la suma de 4 mensajes:
# m1 + m2 + m3 + m4 = hint
# Entonces: m4 = hint - (m1 + m2 + m3)

print("\n[*] Intentando recuperar los mensajes con diferentes valores de e...")

# El exponente e es un primo aleatorio menor que 2^10 = 1024
primes = [p for p in range(2, 1024) if gmpy2.is_prime(p)]
print(f"[+] Hay {len(primes)} primos posibles para e")

# Para cada posible e, intentamos:
# 1. Ver si los cifrados son potencias perfectas
# 2. Ver si podemos calcular el 4to mensaje a partir del hint

for e in primes[:30]:  # Probar los primeros 30 primos
    # Verificar si todos los cifrados son potencias e-ésimas
    roots = []
    all_exact = True
    
    for ct in cts:
        root, is_exact = gmpy2.iroot(ct, e)
        if is_exact:
            roots.append(int(root))
        else:
            all_exact = False
            break
    
    if all_exact:
        print(f"\n[!] Todos los cifrados son potencias {e}-ésimas exactas!")
        
        # Calcular la suma de los 3 mensajes conocidos
        sum_known = sum(roots)
        print(f"[+] Suma de los 3 mensajes conocidos: {sum_known}")
        
        # El 4to mensaje sería:
        m4 = hint - sum_known
        
        if m4 > 0:
            print(f"[+] 4to mensaje calculado: {m4}")
            
            # Mostrar todos los mensajes
            all_messages = roots + [m4]
            for i, m in enumerate(all_messages):
                msg_bytes = long_to_bytes(m)
                print(f"\n[+] Mensaje {i+1}:")
                print(f"    Decimal: {m}")
                print(f"    Hex: {msg_bytes.hex()}")
                try:
                    decoded = msg_bytes.decode('utf-8', errors='ignore')
                    print(f"    Texto: {decoded}")
                    if 'HTB{' in decoded or 'htb{' in decoded:
                        print(f"\n[!!!] FLAG ENCONTRADA: {decoded}")
                except:
                    pass
            
            # Concatenar todos los mensajes
            concatenated = b''.join([long_to_bytes(m) for m in all_messages])
            print(f"\n[+] Todos concatenados: {concatenated}")
            
            break

# Si no encontramos con raíces exactas, intentar aproximación
if not all_exact:
    print("\n[*] No se encontraron raíces exactas. Intentando con Coppersmith...")
    
    # Para mensajes pequeños con exponente pequeño, podríamos usar Coppersmith
    # o simplemente bruteforcear si los mensajes son muy pequeños
    
    print("\n[*] Analizando el tamaño del hint...")
    print(f"[+] Hint tiene {hint.bit_length()} bits")
    print(f"[+] Si dividimos entre 4 mensajes: ~{hint.bit_length()//4} bits por mensaje promedio")
    
    # Si los mensajes son pequeños (< 256 bits cada uno), podríamos intentar bruteforcear
    
    # También podemos intentar con el hecho de que el hint empieza con "c4t|"
    # que parece ASCII legible
    
    print("\n[*] El hint parece contener texto legible al principio...")
    hint_str = long_to_bytes(hint).decode('latin-1', errors='ignore')
    print(f"[+] Hint decodificado: {hint_str}")
    
    # Buscar patrones HTB
    if 'HTB{' in hint_str:
        print("[!!!] El hint contiene la flag directamente!")
    
    # Tal vez necesitamos XOR o alguna operación con el hint
    print("\n[*] Intentando XOR entre cifrados y hint...")
    for i, ct in enumerate(cts):
        xor_result = ct ^ hint
        xor_bytes = long_to_bytes(xor_result)[:50]  # Solo los primeros 50 bytes
        try:
            decoded = xor_bytes.decode('utf-8', errors='ignore')
            if any(c in decoded for c in ['HTB', 'FLAG', 'flag']):
                print(f"[!] XOR cifrado {i+1} con hint: {decoded}")
        except:
            pass