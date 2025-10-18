#!/usr/bin/env python3
import itertools
import string

# Código original simplificado
def process_input(eat):
    """Procesa el input según el código original"""
    if len(eat) != 9:
        return None
    
    EATEATEAT = len(eat) // 3  # 3
    EATEATEATEAT = EATEATEAT + 1  # 4
    EATEATEATEATEAT = EATEATEAT - 1  # 2
    
    # Verificar formato
    if not eat[:EATEATEAT].isdigit():
        return None
    if not eat[len(eat)-EATEATEAT+1:].isdigit():
        return None
    
    # Procesar
    reversed_eat = eat[::-1]
    
    # Ate
    ate_result = "Eat" + str(len(reversed_eat)) + reversed_eat[:EATEATEAT]
    
    # eaT
    multiplied = str(int(eat[:EATEATEAT])*EATEATEAT)
    eat_result = multiplied + reversed_eat
    
    # EAt (intercalar)
    i1 = 0
    i2 = 0
    eateat = 0
    final = ""
    while i1 < len(eat_result) and i2 < len(ate_result):
        if eateat % EATEATEAT == EATEATEATEATEAT // EATEATEAT:
            final += ate_result[i2]
            i2 += 1
        else:
            final += eat_result[i1]
            i1 += 1
        eateat += 1
    
    return final

target = "E10a23t9090t9ae0140"

print(f"Buscando input que genere: {target}")
print(f"Formato: DDDxxxxDD donde D=dígito")
print()

# El formato es DDDxxxxDD
# Los primeros 3 deben ser dígitos
# Los últimos 2 deben ser dígitos
# Las posiciones 3,4,5,6 pueden ser cualquier cosa

# Generar todos los caracteres posibles (letras, dígitos, algunos símbolos)
chars = string.ascii_letters + string.digits

# Fuerza bruta inteligente
# Sabemos que el resultado contiene: E, 0, a, 3, t, 9, e, 1, 4
# Estos caracteres podrían venir del input

# Probemos primero con solo los caracteres que aparecen en el target
target_chars = set(target)
print(f"Caracteres en target: {sorted(target_chars)}")

# Intentemos con combinaciones pequeñas primero
print("\nProbando combinaciones...")

count = 0
found = False

# Los primeros 3 dígitos: 000-999
for first_3_digits in range(1000):
    first_3 = f"{first_3_digits:03d}"
    
    # Los últimos 2 dígitos: 00-99
    for last_2_digits in range(100):
        last_2 = f"{last_2_digits:02d}"
        
        # Las 4 posiciones del medio: probar con caracteres comunes
        # Primero probar con caracteres que aparecen en el target
        for middle in itertools.product(['0', '1', '2', '3', '4', '9', 'a', 'e', 't', 'E'], repeat=4):
            middle_str = ''.join(middle)
            
            input_str = first_3 + middle_str + last_2
            
            result = process_input(input_str)
            
            count += 1
            if count % 10000 == 0:
                print(f"  Probado {count} combinaciones... (último: {input_str})")
            
            if result == target:
                print(f"\n✅ ¡ENCONTRADO!")
                print(f"Input: {input_str}")
                print(f"Resultado: {result}")
                flag = "eaten_" + input_str
                print(f"\n🚩 CTFlearn{{{flag}}}")
                found = True
                break
        
        if found:
            break
    
    if found:
        break
    
    if first_3_digits % 100 == 0:
        print(f"  Progreso: {first_3_digits}/999...")

if not found:
    print("\n❌ No se encontró con fuerza bruta básica")
    print("  Probando con más caracteres...")
