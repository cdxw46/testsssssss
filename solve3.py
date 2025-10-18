#!/usr/bin/env python3

# Voy a simular el intercalado paso a paso

target = "E10a23t9090t9ae0140"
print(f"Target: {target}")
print(f"Longitud del target: {len(target)}")

# Simular el intercalado al revés
def extract_from_interleave(result):
    """Extrae eat y eats del resultado del intercalado"""
    eat_chars = []
    eats_chars = []
    
    for eateat in range(len(result)):
        if eateat % 3 == 1:
            eats_chars.append(result[eateat])
        else:
            eat_chars.append(result[eateat])
    
    return ''.join(eat_chars), ''.join(eats_chars)

eat_str, eats_str = extract_from_interleave(target)
print(f"\neat_str: {eat_str} (longitud {len(eat_str)})")
print(f"eats_str: {eats_str} (longitud {len(eats_str)})")

# Probemos simular el intercalado con estos valores
def simulate_interleave(eat, eats):
    """Simula el intercalado"""
    i1 = 0
    i2 = 0
    eateat = 0
    result = ""
    while i1 < len(eat) and i2 < len(eats):
        if eateat % 3 == 1:
            result += eats[i2]
            i2 += 1
        else:
            result += eat[i1]
            i1 += 1
        eateat += 1
    return result

# Verificar que funciona
recreated = simulate_interleave(eat_str, eats_str)
print(f"\nRecreado: {recreated}")
print(f"Match: {recreated == target}")

# Ahora trabajemos hacia atrás
# eats_str debe ser: "Eat" + str(len(input[::-1])) + input[::-1][:3]
# eat_str debe ser: str(int(input[:3])*3) + input[::-1]

# Si input tiene longitud L, entonces:
# eats_str = "Eat" + str(L) + input[::-1][:3]

# Probemos diferentes longitudes
for L in range(5, 15):
    prefix = "Eat" + str(L)
    if eats_str.startswith(prefix):
        print(f"\n✓ Input tiene longitud {L}")
        reversed_first_3 = eats_str[len(prefix):]
        print(f"input[::-1][:3] = {reversed_first_3}")
        
        # Los últimos 3 de input son (invertidos) reversed_first_3
        if len(reversed_first_3) == 3:
            last_3 = reversed_first_3[::-1]
            print(f"input[-3:] = {last_3}")
        else:
            print(f"ERROR: reversed_first_3 tiene longitud {len(reversed_first_3)}, no 3")
        
        # Ahora desde eat_str
        # eat_str = str(int(input[:3])*3) + input[::-1]
        # input[::-1] tiene longitud L
        
        # Intentemos diferentes longitudes del prefijo multiplicado
        for digit_len in [1, 2, 3, 4]:
            if digit_len + L > len(eat_str):
                continue
            
            if digit_len + L != len(eat_str):
                continue
            
            multiplied = eat_str[:digit_len]
            reversed_input = eat_str[digit_len:]
            
            if not multiplied.isdigit():
                continue
            
            mult_val = int(multiplied)
            if mult_val % 3 != 0:
                continue
            
            orig_val = mult_val // 3
            
            # input[:3] debería ser str(orig_val) con padding adecuado
            # Intentemos con 3 dígitos (con ceros a la izquierda si es necesario)
            first_3 = f"{orig_val:03d}"
            
            if len(first_3) != 3:
                continue
            
            # Reconstruir input
            input_candidate = reversed_input[::-1]
            
            # Verificar que input[:3] coincide
            if input_candidate[:3] != first_3:
                print(f"  Intentando digit_len={digit_len}: input[:3]={input_candidate[:3]} != {first_3}")
                continue
            
            # Verificar longitud
            if len(input_candidate) != L:
                print(f"  Intentando digit_len={digit_len}: longitud incorrecta {len(input_candidate)} != {L}")
                continue
            
            # Verificar que reversed_first_3 coincide
            if input_candidate[::-1][:3] != reversed_first_3:
                print(f"  Intentando digit_len={digit_len}: reversed mismatch")
                continue
            
            print(f"\n🎯 Candidato encontrado con digit_len={digit_len}:")
            print(f"  multiplied: {multiplied} = {first_3} * 3")
            print(f"  reversed_input: {reversed_input}")
            print(f"  input: {input_candidate}")
            
            # Verificar condiciones del código original
            if L == 9:
                if not input_candidate[:3].isdigit():
                    print("  ❌ Primeros 3 no son dígitos")
                    continue
                if not input_candidate[7:].isdigit():
                    print("  ❌ Caracteres 7-8 no son dígitos")
                    continue
            
            # Verificar procesando completamente
            def full_process(inp):
                rev = inp[::-1]
                eats_result = "Eat" + str(len(rev)) + rev[:3]
                eat_result = str(int(inp[:3])*3) + rev
                result = simulate_interleave(eat_result, eats_result)
                return result
            
            result = full_process(input_candidate)
            print(f"  Resultado: {result}")
            print(f"  Target:    {target}")
            print(f"  Match: {result == target}")
            
            if result == target:
                print(f"\n✅ ¡SOLUCIÓN ENCONTRADA!")
                flag = "eaten_" + input_candidate
                print(f"\n🚩 CTFlearn{{{flag}}}")
                exit(0)

print("\n❌ No se encontró solución")
