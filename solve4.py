#!/usr/bin/env python3

target = "E10a23t9090t9ae0140"

# Para generar 19 caracteres con intercalado:
# Necesito eat con 13 chars y eats con 7 chars
# (o más, pero al menos esos)

# Simulación más cuidadosa
def simulate_interleave(eat, eats, max_iterations=100):
    """Simula el intercalado"""
    i1 = 0
    i2 = 0
    eateat = 0
    result = ""
    
    while i1 < len(eat) and i2 < len(eats) and eateat < max_iterations:
        if eateat % 3 == 1:
            result += eats[i2]
            i2 += 1
        else:
            result += eat[i1]
            i1 += 1
        eateat += 1
    
    return result

# Determinar qué longitudes necesito para generar target
# Probar diferentes combinaciones
for eat_len in range(10, 20):
    for eats_len in range(5, 15):
        # Extraer caracteres asumiendo estas longitudes
        eat_chars = []
        eats_chars = []
        
        i1 = 0
        i2 = 0
        for eateat in range(len(target)):
            if eateat % 3 == 1:
                if i2 < eats_len:
                    eats_chars.append(target[eateat])
                    i2 += 1
                else:
                    break  # eats se agotó
            else:
                if i1 < eat_len:
                    eat_chars.append(target[eateat])
                    i1 += 1
                else:
                    break  # eat se agotó
            
            # Verificar si ambos están agotados
            if i1 >= eat_len or i2 >= eats_len:
                break
        
        eat_str = ''.join(eat_chars)
        eats_str = ''.join(eats_chars)
        
        # Verificar si al simular obtenemos el target
        simulated = simulate_interleave(eat_str, eats_str)
        
        if simulated == target:
            print(f"✓ Encontrado: eat_len={eat_len}, eats_len={eats_len}")
            print(f"  eat_str: {eat_str} (len={len(eat_str)})")
            print(f"  eats_str: {eats_str} (len={len(eats_str)})")
            
            # Ahora resolver para el input
            # eats_str = "Eat" + str(L) + input[::-1][:3]
            # eat_str = str(int(input[:3])*3) + input[::-1]
            
            # Probar diferentes longitudes de input
            for L in range(5, 15):
                prefix = "Eat" + str(L)
                if not eats_str.startswith(prefix):
                    continue
                
                reversed_first_3 = eats_str[len(prefix):]
                if len(reversed_first_3) != 3:
                    continue
                
                print(f"\n  Input longitud: {L}")
                print(f"  input[::-1][:3] = {reversed_first_3}")
                
                # Probar diferentes longitudes del prefijo multiplicado en eat_str
                for digit_len in [1, 2, 3, 4]:
                    if digit_len + L != len(eat_str):
                        continue
                    
                    multiplied = eat_str[:digit_len]
                    if not multiplied.isdigit():
                        continue
                    
                    reversed_input = eat_str[digit_len:]
                    if len(reversed_input) != L:
                        continue
                    
                    mult_val = int(multiplied)
                    if mult_val % 3 != 0:
                        continue
                    
                    orig_val = mult_val // 3
                    first_3 = f"{orig_val:03d}"
                    
                    if len(first_3) != 3:
                        continue
                    
                    # Reconstruir input
                    input_candidate = reversed_input[::-1]
                    
                    # Verificar consistencia
                    if input_candidate[:3] != first_3:
                        continue
                    if input_candidate[::-1][:3] != reversed_first_3:
                        continue
                    
                    print(f"\n  🎯 Candidato: {input_candidate}")
                    
                    # Verificar procesamiento completo
                    def full_process(inp):
                        rev = inp[::-1]
                        eats_result = "Eat" + str(len(rev)) + rev[:3]
                        eat_result = str(int(inp[:3])*3) + rev
                        return simulate_interleave(eat_result, eats_result)
                    
                    result = full_process(input_candidate)
                    print(f"  Resultado: {result}")
                    print(f"  Target:    {target}")
                    
                    if result == target:
                        # Verificar condiciones adicionales
                        if L == 9:
                            if not input_candidate[:3].isdigit():
                                print("  ❌ Primeros 3 no son dígitos")
                                continue
                            if not input_candidate[7:9].isdigit():
                                print("  ❌ Caracteres 7-8 no son dígitos")
                                continue
                        
                        print(f"\n  ✅ ¡SOLUCIÓN CORRECTA!")
                        flag = "eaten_" + input_candidate
                        print(f"\n  🚩 CTFlearn{{{flag}}}")
                        exit(0)

print("\n❌ No se encontró solución")
