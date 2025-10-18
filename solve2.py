#!/usr/bin/env python3

# Voy a simular el intercalado más cuidadosamente

target = "E10a23t9090t9ae0140"

# El intercalado se hace así:
# eateat=0: % 3 = 0 != 1 -> toma de eat[0]
# eateat=1: % 3 = 1 == 1 -> toma de eats[0]
# eateat=2: % 3 = 2 != 1 -> toma de eat[1]
# eateat=3: % 3 = 0 != 1 -> toma de eat[2]
# eateat=4: % 3 = 1 == 1 -> toma de eats[1]
# ...

# Entonces el patrón es: eat, eats, eat, eat, eats, eat, eat, eats, ...
# Posiciones:             0     1     2    3     4     5    6     7

# Extraigamos qué viene de dónde
eat_indices = []
eats_indices = []

for i in range(len(target)):
    if i % 3 == 1:
        eats_indices.append(i)
    else:
        eat_indices.append(i)

print("Índices de eat:", eat_indices)
print("Índices de eats:", eats_indices)

eat_chars = [target[i] for i in eat_indices]
eats_chars = [target[i] for i in eats_indices]

eat_str = ''.join(eat_chars)
eats_str = ''.join(eats_chars)

print(f"\neat debe aportar: {eat_str}")
print(f"eats debe aportar: {eats_str}")

# Ahora:
# eats = "Eat9" + reversed_input[:3]
# eat = str(int(input[:3])*3) + reversed_input

# De eats_str podemos extraer reversed_input[:3]:
if eats_str.startswith("Eat9"):
    reversed_first_3 = eats_str[4:]
    print(f"\nreversed_input[:3] = {reversed_first_3}")
    
    # reversed_input[:3] son los primeros 3 de input invertido
    # O sea, los últimos 3 de input invertidos
    # input[-3:] invertido = reversed_first_3
    # input[-3:] = reversed_first_3[::-1]
    last_3 = reversed_first_3[::-1]
    print(f"input[-3:] = {last_3}")
    
    # De eat_str podemos extraer: str(int(input[:3])*3) + reversed_input
    # reversed_input tiene 9 caracteres
    # eat_str = dígitos + reversed_input[3:]  (porque ya usamos los primeros 3 en eats)
    
    # ¿O es que eat_str contiene TODO reversed_input?
    # Sí, debería contener TODO reversed_input completo
    
    # eat_str = str(int(input[:3])*3) + reversed_input
    # reversed_input tiene 9 chars
    # eat_str debería tener longitud: 2-3 dígitos + 9 = 11-12
    
    print(f"Longitud de eat_str: {len(eat_str)}")
    
    # Si input[:3] es 3 dígitos, int puede ser de 0 a 999
    # * 3 -> 0 a 2997
    # str de eso: 1 a 4 dígitos
    
    # Probemos diferentes longitudes de la parte multiplicada
    for digit_len in [1, 2, 3, 4]:
        if digit_len >= len(eat_str):
            continue
        
        multiplied_str = eat_str[:digit_len]
        reversed_input = eat_str[digit_len:]
        
        if not multiplied_str.isdigit():
            continue
        
        if len(reversed_input) != 9:
            continue
        
        multiplied_val = int(multiplied_str)
        
        # multiplied_val debe ser divisible por 3
        if multiplied_val % 3 != 0:
            continue
        
        original_val = multiplied_val // 3
        
        # input[:3] como string con padding si es necesario
        # Probemos diferentes formatos
        for fmt in ["{:01d}", "{:02d}", "{:03d}"]:
            first_3 = fmt.format(original_val)
            if len(first_3) > 3:
                continue
            if len(first_3) < 3:
                continue
            
            # Construir input
            input_str = reversed_input[::-1]
            
            # input[:3] debería ser first_3
            if input_str[:3] != first_3:
                continue
            
            # input[-3:] debería ser last_3
            if input_str[-3:] != last_3:
                continue
            
            print(f"\n🎯 Candidato encontrado!")
            print(f"Dígitos multiplicados: {multiplied_str} = {first_3} * 3")
            print(f"reversed_input: {reversed_input}")
            print(f"input: {input_str}")
            
            # Verificar condiciones adicionales
            if not input_str[:3].isdigit():
                print("❌ Los primeros 3 no son dígitos")
                continue
            
            if not input_str[7:].isdigit():
                print("❌ Los últimos 2 (posiciones 7-8) no son dígitos")
                continue
            
            # Verificar procesando
            def verify(inp):
                reversed_inp = inp[::-1]
                ate_result = "Eat" + str(len(reversed_inp)) + reversed_inp[:3]
                eat_result = str(int(inp[:3])*3) + reversed_inp
                
                # Intercalar
                i1 = 0
                i2 = 0
                eateat = 0
                result = ""
                while i1 < len(eat_result) and i2 < len(ate_result):
                    if eateat % 3 == 1:
                        result += ate_result[i2]
                        i2 += 1
                    else:
                        result += eat_result[i1]
                        i1 += 1
                    eateat += 1
                return result
            
            result = verify(input_str)
            print(f"Resultado: {result}")
            print(f"Target:    {target}")
            
            if result == target:
                print(f"\n✅ ¡CORRECTO!")
                flag = "eaten_" + input_str
                print(f"FLAG: CTFlearn{{{flag}}}")
                break
else:
    print("eats_str no comienza con 'Eat9'")
    print(f"eats_str = {eats_str}")
    
    # Tal vez la longitud no es 9? Probemos otras longitudes
    for length in range(7, 12):
        prefix = "Eat" + str(length)
        if eats_str.startswith(prefix):
            print(f"Longitud del input: {length}")
            break
