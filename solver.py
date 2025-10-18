#!/usr/bin/env python3

# Analizando el código ofuscado
# Con input de 9 caracteres:
# EATEATEAT = 9//3 = 3
# EATEATEATEAT = 3+1 = 4
# EATEATEATEATEAT = 3-1 = 2

# Funciones renombradas para claridad:
def multiply_by_3(eat):
    """Eating: str(int(eat)*3)"""
    return str(int(eat)*3)

def interleave(eat, eats):
    """EAt: Intercala dos strings basándose en eateat % 3 == 1"""
    print(f"Interleaving: {eat} and {eats}")
    eat1 = 0
    eat2 = 0
    eateat = 0
    result = ""
    while eat1 < len(eat) and eat2 < len(eats):
        if eateat % 3 == 1:  # 4//3 = 1
            result += eats[eat2]
            eat2 += 1
        else:
            result += eat[eat1]
            eat1 += 1
        eateat += 1
    print(f"Result: {result}")
    return result

def reverse(eat):
    """aten: eat[::3-4] = eat[::-1]"""
    return eat[::-1]

def process_eat(eat):
    """eaT: multiply_by_3(eat[:3]) + reverse(eat)"""
    return multiply_by_3(eat[:3]) + reverse(eat)

def identity(eat):
    """aTE: simplemente retorna eat"""
    return eat

def make_ate(eat):
    """Ate: "Eat" + str(len(eat)) + eat[:3]"""
    return "Eat" + str(len(eat)) + eat[:3]

# El objetivo es que interleave(process_eat(eat), make_ate(identity(reverse(eat))))
# debe dar "E10a23t9090t9ae0140"

target = "E10a23t9090t9ae0140"

# El formato del input debe ser: DDDxxxxDD (9 caracteres)
# donde D = dígito, x = cualquier cosa
# eat[:3] debe ser dígitos
# eat[7:] debe ser dígitos

# Probemos con fuerza bruta inteligente
def test_input(eat):
    """Verifica si el input genera el target"""
    if len(eat) != 9:
        return False
    if not eat[:3].isdigit():
        return False
    if not eat[7:].isdigit():
        return False
    
    # Procesar
    reversed_eat = reverse(eat)
    ate_part = make_ate(identity(reversed_eat))
    eat_part = process_eat(eat)
    result = interleave(eat_part, ate_part)
    
    return result == target

# Analicemos el target: "E10a23t9090t9ae0140"
# Longitud: 21 caracteres

# Veamos el patrón de intercalado:
# eateat % 3 == 1: posiciones 1, 4, 7, 10, 13, 16, 19 vienen de eats
# otras posiciones vienen de eat

# Posiciones de target:
# 0:E  1:1  2:0  3:a  4:2  5:3  6:t  7:9  8:0  9:9  10:0  11:t  12:9  13:a  14:e  15:0  16:1  17:4  18:0
# 
# De eats (pos 1,4,7,10,13,16): 1, 2, 9, 0, a, 1
# De eat  (pos 0,2,3,5,6,8,9,11,12,14,15,17,18): E, 0, a, 3, t, 0, 9, t, 9, e, 0, 4, 0

# Entonces:
# eat_part debería ser: "E0a3t09t9e040" (13 chars)
# ate_part debería ser: "129a1" pero necesitamos más caracteres...

# Espera, el intercalado continúa mientras ambos tengan caracteres.
# Si eat_part tiene más, se usan al final.

# Reconstruyamos mejor:
positions_from_eats = []  # posiciones donde eateat % 3 == 1
positions_from_eat = []   # otras posiciones

for eateat in range(21):
    if eateat % 3 == 1:
        positions_from_eats.append(eateat)
    else:
        positions_from_eat.append(eateat)

print("Positions from eats:", positions_from_eats)  # 1, 4, 7, 10, 13, 16, 19
print("Positions from eat:", positions_from_eat)    # 0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20

# Extraer caracteres del target
eats_chars = [target[i] for i in positions_from_eats]
eat_chars = [target[i] for i in positions_from_eat]

print("Characters from eats:", ''.join(eats_chars))  # lo que debe venir de ate_part
print("Characters from eat:", ''.join(eat_chars))    # lo que debe venir de eat_part

# ate_part = "Eat" + str(len(reversed_eat)) + reversed_eat[:3]
# Si eat tiene 9 caracteres, ate_part = "Eat9" + reversed_eat[:3]
# ate_part tiene longitud 7

# eat_part = multiply_by_3(eat[:3]) + reverse(eat)
# eat_part tiene longitud: 2 o 3 (dígitos *3) + 9 = 11-12 caracteres

print("\nLet's solve it:")
eats_target = ''.join(eats_chars)  # "1290a10"
eat_target = ''.join(eat_chars)    # "E0a3t09t9e040"

print(f"ate_part should be: {eats_target}")
print(f"eat_part should be: {eat_target}")

# ate_part = "Eat9" + reversed_eat[:3]
# "Eat9" + reversed_eat[:3] = "1290a10"
# Esto no coincide... "Eat9" tiene 4 caracteres, necesitamos "1290a10" (7 chars)

# Revisemos: la función interleave puede tener más caracteres en uno que otro
# Miremos solo los primeros caracteres realmente intercalados

# Intentemos resolver manualmente:
# eat_part comienza con "E0a3t09t9e040"
# ate_part comienza con "1290a10"...

# Si eat = "123xyz45", entonces:
# reversed_eat = "54zyx321"
# ate_part = "Eat9" + "54z" = "Eat954z"
# eat_part = str(int("123")*3) + "54zyx321" = "369" + "54zyx321" = "36954zyx321"

# Probemos con búsqueda inteligente
# eat_part debe empezar con E... pero multiply_by_3 genera dígitos!
# A menos que... espera, revisemos el código original

