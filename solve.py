#!/usr/bin/env python3

# Reconstruyendo las funciones con los valores conocidos
# Para input de 9 caracteres: EATEATEAT=3, EATEATEATEAT=4, EATEATEATEATEAT=2

def process_funcs(eat):
    """Simula el procesamiento completo"""
    # aten: reverse
    reversed_eat = eat[::-1]
    
    # aTE: identity
    ate_input = reversed_eat
    
    # Ate: "Eat" + str(len) + primeros 3
    ate_result = "Eat" + str(len(ate_input)) + ate_input[:3]
    
    # eaT: str(int(primeros 3)*3) + reversed
    eat_result = str(int(eat[:3])*3) + reversed_eat
    
    # EAt: intercalar
    eat1 = 0
    eat2 = 0
    eateat = 0
    result = ""
    while eat1 < len(eat_result) and eat2 < len(ate_result):
        if eateat % 3 == 1:
            result += ate_result[eat2]
            eat2 += 1
        else:
            result += eat_result[eat1]
            eat1 += 1
        eateat += 1
    
    return result

# Target
target = "E10a23t9090t9ae0140"

# Extraer componentes del intercalado
eat_chars = []
ate_chars = []

for i in range(len(target)):
    if i % 3 == 1:
        ate_chars.append(target[i])
    else:
        eat_chars.append(target[i])

eat_part = ''.join(eat_chars)
ate_part = ''.join(ate_chars)

print(f"eat_part debe ser: {eat_part}")
print(f"ate_part debe ser: {ate_part}")
print(f"Longitudes: eat={len(eat_part)}, ate={len(ate_part)}")

# ate_part = "Eat9" + reversed_eat[:3]
# ate_part tiene que ser lo que extrajimos

# eat_part = str(int(eat[:3])*3) + eat[::-1]

# Sabemos que ate_part comienza con "Eat9" (porque len=9)
# Entonces reversed_eat[:3] son los caracteres restantes de ate_part después de "Eat9"

ate_without_prefix = ate_part[4:]  # quitar "Eat9"
print(f"\nreversed_eat[:3] debe ser: {ate_without_prefix}")

# reversed_eat[:3] = primeros 3 chars de reversed_eat
# Si eat = "abcdefghi", reversed_eat = "ihgfedcba", reversed_eat[:3] = "ihg"

# Entonces los últimos 3 caracteres de eat son (reversed): ate_without_prefix
# eat[-3:] al revés = ate_without_prefix
eat_suffix = ate_without_prefix[::-1]
print(f"eat[-3:] debe ser: {eat_suffix}")

# Ahora para eat_part:
# eat_part = str(int(eat[:3])*3) + eat[::-1]

# Sabemos que eat[:3] son dígitos (condición del código)
# eat[7:] son dígitos (últimos 2 chars)

# Entonces eat tiene formato: DDDxxxxDD donde los últimos 3 son el eat_suffix calculado

# eat = "DDDxx" + eat_suffix
# Necesitamos que los últimos 2 de eat_suffix sean dígitos
# eat_suffix ya lo tenemos

# Verifiquemos si el suffix tiene dígitos al final
if len(eat_suffix) >= 2:
    print(f"Últimos 2 chars de eat: {eat_suffix[-2:]}")
    if eat_suffix[-2:].isdigit():
        print("✓ Los últimos 2 son dígitos")
    else:
        print("✗ Los últimos 2 NO son dígitos")

# eat_part = str(int(eat[:3])*3) + eat[::-1]
# eat[::-1] = reversed_eat

# eat_part empieza con dígitos (el resultado de int*3), luego reversed_eat

# Intentemos extraer cuántos dígitos hay al inicio de eat_part
digit_count = 0
for c in eat_part:
    if c.isdigit():
        digit_count += 1
    else:
        break

print(f"\nDígitos al inicio de eat_part: {digit_count}")
multiplied = eat_part[:digit_count]
reversed_eat = eat_part[digit_count:]

print(f"str(int(eat[:3])*3) = {multiplied}")
print(f"reversed_eat = {reversed_eat}")

# Calcular eat[:3]
if multiplied.isdigit():
    original_first_three = int(multiplied) // 3
    print(f"eat[:3] = {original_first_three:03d}")
    
    # eat = eat[:3] + middle + eat[-3:]
    # reversed_eat = eat[::-1]
    # eat = reversed_eat[::-1]
    eat = reversed_eat[::-1]
    print(f"\neat calculado: {eat}")
    
    # Verificar
    result = process_funcs(eat)
    print(f"\nResultado: {result}")
    print(f"Target:    {target}")
    print(f"Match: {result == target}")
    
    if result == target:
        flag = "eaten_" + eat
        print(f"\n🚩 FLAG: CTFlearn{{{flag}}}")
