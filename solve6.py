#!/usr/bin/env python3
from Crypto.Util.number import *
import gmpy2

# Datos del output
N = 5981664384988507891478572449251897296717727847212579781448791472718547112403550208352320926002397616312181279859738938646168022481824206589739320298482728968548378237391009138243024910596491172979923991673446034011260330224409794208875199561844435663744993504673450898288161482849187018770655419007178851937895764901674192425054643548670616348302447202491340266057221307744866082461604674766259695903766772980842036324667567850124019171425634526227426965833985082234968255176231124754301435374519312001547854794352023852342682220352109083558778402466358598254431167382653831478713628185748237886560605604945010671417

cts = [4064195644006411160585797813860027634920635349984344191047587061586620848352019080467087592184982883284356841385019453458842500930190512793665886381102812026066865666098391973664302897278510995945377153937248437062600080527317980210967973971371047319247120004523147629534186514628527555180736833194525516718549330721987873868571634294877416190209288629499265010822332662061001208360467692613959936438519512705706688327846470352610192922218603268096313278741647626899523312431823527174576009143724850631439559205050395629961996905961682800070679793831568617438035643749072976096500278297683944583609092132808342160168, 3972397619896893471633226994966440180689669532336298201562465946694941720775869427764056001983618377003841446300122954561092878433908258359050016399257266833626893700179430172867058140215023211349613449750819959868861260714924524414967854467488908710563470522800186889553825417008118394349306170727982570843758792622898850338954039322560740348595654863475541846505121081201633770673996898756298398831948133434844321091554344145679504115839940880338238034227536355386474785852916335583794757849746186832609785626770517073108801492522816245458992502698143396049695921044554959802743742110180934416272358039695942552488, 956566266150449406104687131427865505474798294715598448065695308619216559681163085440476088324404921175885831054464222377255942505087330963629877648302727892001779224319839877897857215091085980519442914974498275528112936281916338633178398286676523416008365096599844169979821513770606168325175652094633129536643417367820830724397070621662683223203491074814734747601002376621653739871373924630026694962642922871008486127796621355314581093953946913681152270251669050414866366693593651789709229310574005739535880988490183275291507128529820194381392682870291338920077175831052974790596134745552552808640002791037755434586]

hint = 2674558878275613295915981392537201653631411909654166620884912623530781

print("[+] Información clave:")
print(f"    - El código original habla de 4 mensajes (pts)")
print(f"    - Solo tenemos 3 cifrados en el output")
print(f"    - El hint es la suma de TODOS los mensajes")
print(f"    - El hint tiene solo 231 bits (muy pequeño)")

hint_bytes = long_to_bytes(hint)
print(f"\n[+] Hint como bytes: {hint_bytes}")
print(f"[+] Hint hex: {hint_bytes.hex()}")

# El hint comienza con "c4t|" que podría ser parte de la flag
# Si los mensajes son tan pequeños (231 bits totales para 4 mensajes)
# entonces cada mensaje es de aproximadamente 58 bits

# Para mensajes tan pequeños, el ataque de Coppersmith puede funcionar
# O simplemente podemos intentar con exponentes pequeños

print("\n[*] Intentando con e=3 y mensajes pequeños...")

# Para e=3, si m < N^(1/3), entonces c = m^3 (sin módulo)
# Pero ya verificamos que no son cubos perfectos

# Sin embargo, si los mensajes son pequeños, podemos usar Coppersmith
# o el hecho de que c = m^e mod N pero m^e podría ser solo ligeramente mayor que N

# Intentemos con la técnica de añadir múltiplos de N
for e in [3, 5, 7]:
    print(f"\n[*] Probando con e={e}...")
    
    # Para cada cifrado, intentar encontrar la raíz
    messages = []
    for i, ct in enumerate(cts):
        found = False
        
        # Probar con múltiplos de N (hasta k*N donde k es razonable para mensajes pequeños)
        # Si m es de ~58 bits y e=3, entonces m^3 es de ~174 bits
        # N es de 2046 bits, así que m^3 << N
        # Pero si c = m^e mod N, y m es pequeño, entonces c = m^e - k*N para algún k pequeño
        
        # Intentar c + k*N para k = 0, 1, 2, ...
        for k in range(0, 100):
            test_value = ct + k * N
            root, is_exact = gmpy2.iroot(test_value, e)
            
            if is_exact:
                print(f"[!] Encontrado mensaje {i+1} con k={k}: {root}")
                messages.append(int(root))
                found = True
                break
        
        if not found:
            # Si no encontramos con suma, intentar con resta
            for k in range(1, 10):
                if ct > k * N:
                    test_value = ct - k * N
                    root, is_exact = gmpy2.iroot(test_value, e)
                    
                    if is_exact:
                        print(f"[!] Encontrado mensaje {i+1} con k=-{k}: {root}")
                        messages.append(int(root))
                        found = True
                        break
        
        if not found:
            break
    
    if len(messages) == 3:
        # Tenemos los 3 mensajes, calculemos el 4to
        sum_3 = sum(messages)
        message_4 = hint - sum_3
        
        print(f"\n[+] Suma de los 3 mensajes: {sum_3}")
        print(f"[+] 4to mensaje calculado: {message_4}")
        
        if message_4 > 0 and message_4 < 2**64:  # Verificar que sea razonable
            messages.append(message_4)
            
            print("\n[+] Todos los mensajes encontrados:")
            for i, m in enumerate(messages):
                msg_bytes = long_to_bytes(m)
                print(f"    Mensaje {i+1}: {msg_bytes}")
                print(f"    Hex: {msg_bytes.hex()}")
            
            # Concatenar todos
            all_msg = b''.join([long_to_bytes(m) for m in messages])
            print(f"\n[+] Concatenados: {all_msg}")
            
            # Buscar la flag
            for m in messages:
                msg = long_to_bytes(m).decode('utf-8', errors='ignore')
                if 'HTB{' in msg:
                    print(f"\n[!!!] FLAG ENCONTRADA: {msg}")
                    break
            else:
                # Si no está en los mensajes individuales, podría estar en la concatenación
                concat_str = all_msg.decode('utf-8', errors='ignore')
                if 'HTB{' in concat_str:
                    print(f"\n[!!!] FLAG ENCONTRADA en concatenación: {concat_str}")
            
            break

# Si nada funcionó hasta ahora, intentemos analizar el patrón del hint
print("\n[*] Analizando el patrón del hint más detalladamente...")
print(f"[+] El hint empieza con 'c4t|'")
print(f"[+] Esto podría ser parte de 'quick_maffs_c4t|...' o similar")

# Intentemos decodificar el hint como si fuera la flag directamente
hint_str = hint_bytes.decode('latin-1')
print(f"[+] Hint completo decodificado: {repr(hint_str)}")

# Buscar patrones de flag
if any(pattern in hint_str for pattern in ['HTB', 'FLAG', 'flag']):
    print("[!!!] El hint contiene patrones de flag!")

# El hint podría ser la concatenación directa de los mensajes
# O podría necesitar alguna transformación