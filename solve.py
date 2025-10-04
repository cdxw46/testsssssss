#!/usr/bin/env python3
from Crypto.Util.number import *
import gmpy2
from sympy import symbols, solve, Integer
import itertools

# Datos del output
N = 5981664384988507891478572449251897296717727847212579781448791472718547112403550208352320926002397616312181279859738938646168022481824206589739320298482728968548378237391009138243024910596491172979923991673446034011260330224409794208875199561844435663744993504673450898288161482849187018770655419007178851937895764901674192425054643548670616348302447202491340266057221307744866082461604674766259695903766772980842036324667567850124019171425634526227426965833985082234968255176231124754301435374519312001547854794352023852342682220352109083558778402466358598254431167382653831478713628185748237886560605604945010671417

cts = [4064195644006411160585797813860027634920635349984344191047587061586620848352019080467087592184982883284356841385019453458842500930190512793665886381102812026066865666098391973664302897278510995945377153937248437062600080527317980210967973971371047319247120004523147629534186514628527555180736833194525516718549330721987873868571634294877416190209288629499265010822332662061001208360467692613959936438519512705706688327846470352610192922218603268096313278741647626899523312431823527174576009143724850631439559205050395629961996905961682800070679793831568617438035643749072976096500278297683944583609092132808342160168, 3972397619896893471633226994966440180689669532336298201562465946694941720775869427764056001983618377003841446300122954561092878433908258359050016399257266833626893700179430172867058140215023211349613449750819959868861260714924524414967854467488908710563470522800186889553825417008118394349306170727982570843758792622898850338954039322560740348595654863475541846505121081201633770673996898756298398831948133434844321091554344145679504115839940880338238034227536355386474785852916335583794757849746186832609785626770517073108801492522816245458992502698143396049695921044554959802743742110180934416272358039695942552488, 956566266150449406104687131427865505474798294715598448065695308619216559681163085440476088324404921175885831054464222377255942505087330963629877648302727892001779224319839877897857215091085980519442914974498275528112936281916338633178398286676523416008365096599844169979821513770606168325175652094633129536643417367820830724397070621662683223203491074814734747601002376621653739871373924630026694962642922871008486127796621355314581093953946913681152270251669050414866366693593651789709229310574005739535880988490183275291507128529820194381392682870291338920077175831052974790596134745552552808640002791037755434586]

hint = 2674558878275613295915981392537201653631411909654166620884912623530781

print("[+] Analizando el problema RSA...")
print(f"[+] N tiene {N.bit_length()} bits")
print(f"[+] Tenemos {len(cts)} cifrados")
print(f"[+] Hint (suma de mensajes planos): {hint}")

# Primero vamos a intentar factorizar N
print("\n[+] Intentando factorizar N...")

# Intentar factorizar con métodos básicos
import primefac
from functools import reduce

def try_factor_n():
    # Intentar con Fermat
    print("[*] Probando método de Fermat...")
    a = gmpy2.isqrt(N)
    if a * a < N:
        a += 1
    
    for i in range(1000000):
        b2 = a * a - N
        if gmpy2.is_square(b2):
            b = gmpy2.isqrt(b2)
            p = a - b
            q = a + b
            if p * q == N:
                print(f"[!] Factorización encontrada!")
                print(f"[+] p = {p}")
                print(f"[+] q = {q}")
                return p, q
        a += 1
    
    return None, None

p, q = try_factor_n()

if p is None:
    print("[*] Fermat no funcionó, intentando otros métodos...")
    
    # Intentar con Pollard Rho
    def pollard_rho(n, max_iter=100000):
        if n % 2 == 0:
            return 2
        x = 2
        y = 2
        d = 1
        f = lambda x: (x**2 + 1) % n
        
        for _ in range(max_iter):
            x = f(x)
            y = f(f(y))
            d = gmpy2.gcd(abs(x - y), n)
            if d != 1 and d != n:
                return d
        return None
    
    factor = pollard_rho(N)
    if factor:
        p = factor
        q = N // p
        print(f"[!] Factorización encontrada con Pollard Rho!")
        print(f"[+] p = {p}")
        print(f"[+] q = {q}")

# Si no podemos factorizar, intentamos otro enfoque
if p is None:
    print("\n[*] No se pudo factorizar N directamente...")
    print("[*] Intentando ataque de Hastad modificado...")
    
    # Dado que tenemos 4 cifrados del mismo mensaje con el mismo e
    # y conocemos la suma, podemos intentar encontrar e
    
    # e es un primo aleatorio menor que 2^10 = 1024
    print("[*] Buscando exponente e (primo < 1024)...")
    
    primes = []
    for i in range(2, 1024):
        if gmpy2.is_prime(i):
            primes.append(i)
    
    print(f"[+] Hay {len(primes)} primos candidatos para e")
    
    # Para cada posible e, intentamos resolver
    for e in primes:
        # Intentar ataque de Hastad
        # Si m^e = c mod N para mensajes pequeños, podríamos recuperar m
        
        # Verificar si algún cifrado es vulnerable
        for i, c in enumerate(cts):
            # Intentar raíz e-ésima
            m_candidate, exact = gmpy2.iroot(c, e)
            if exact:
                print(f"[!] Encontrado mensaje {i+1} con e={e}: {m_candidate}")
                
        # También podemos intentar con la relación de la suma
        # Si tenemos m1 + m2 + m3 + m4 = hint
        # Y cada mi^e = ci mod N
        
        # Para mensajes pequeños, podríamos tener mi^e < N
        # En ese caso ci = mi^e (sin módulo)
        all_exact = True
        ms = []
        for c in cts:
            m, exact = gmpy2.iroot(c, e)
            if not exact:
                all_exact = False
                break
            ms.append(m)
        
        if all_exact:
            if sum(ms) == hint:
                print(f"\n[!] ÉXITO! Encontrados todos los mensajes con e={e}")
                for i, m in enumerate(ms):
                    print(f"[+] Mensaje {i+1}: {m}")
                    try:
                        flag = long_to_bytes(m).decode('utf-8', errors='ignore')
                        print(f"[+] Decodificado: {flag}")
                        if 'HTB{' in flag or 'htb{' in flag or 'flag{' in flag:
                            print(f"\n[!!!] FLAG ENCONTRADA: {flag}")
                    except:
                        pass
                break
else:
    # Si tenemos p y q, podemos calcular phi y encontrar d para cada posible e
    phi = (p - 1) * (q - 1)
    print(f"\n[+] phi(N) = {phi}")
    
    # Probar cada posible e
    primes = []
    for i in range(2, 1024):
        if gmpy2.is_prime(i) and gmpy2.gcd(i, phi) == 1:
            primes.append(i)
    
    print(f"[+] Probando {len(primes)} valores posibles de e...")
    
    for e in primes:
        d = gmpy2.invert(e, phi)
        
        # Descifrar todos los mensajes
        pts_candidate = []
        for c in cts:
            m = pow(c, d, N)
            pts_candidate.append(m)
        
        # Verificar si la suma coincide
        if sum(pts_candidate) == hint:
            print(f"\n[!] ÉXITO! e = {e}")
            print(f"[+] d = {d}")
            
            for i, m in enumerate(pts_candidate):
                print(f"\n[+] Mensaje {i+1}: {m}")
                try:
                    decoded = long_to_bytes(m).decode('utf-8', errors='ignore')
                    print(f"[+] Decodificado: {decoded}")
                    if 'HTB{' in decoded or 'htb{' in decoded or 'flag{' in decoded:
                        print(f"\n[!!!] FLAG ENCONTRADA: {decoded}")
                except:
                    pass
            break

print("\n[+] Script terminado.")