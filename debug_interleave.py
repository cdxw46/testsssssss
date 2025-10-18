#!/usr/bin/env python3

def simulate_interleave_debug(eat, eats):
    """Simula el intercalado con debug"""
    print(f"\nIntercalando:")
    print(f"  eat: {eat} (len={len(eat)})")
    print(f"  eats: {eats} (len={len(eats)})")
    
    i1 = 0
    i2 = 0
    eateat = 0
    result = ""
    
    while i1 < len(eat) and i2 < len(eats):
        if eateat % 3 == 1:
            char = eats[i2]
            result += char
            print(f"  eateat={eateat:2d}: eats[{i2}]='{char}' -> result='{result}'")
            i2 += 1
        else:
            char = eat[i1]
            result += char
            print(f"  eateat={eateat:2d}: eat[{i1}]='{char}'  -> result='{result}'")
            i1 += 1
        eateat += 1
    
    print(f"  Bucle termina: i1={i1}, i2={i2}, eateat={eateat}")
    print(f"  Resultado final: {result} (len={len(result)})")
    return result

# Test
eat_str = "E0a3t09t9e040"
eats_str = "1290a1"

result = simulate_interleave_debug(eat_str, eats_str)

target = "E10a23t9090t9ae0140"
print(f"\nTarget: {target} (len={len(target)})")
print(f"Match: {result == target}")

# Analizar diferencias
if result != target:
    print(f"\nDiferencias:")
    max_len = max(len(result), len(target))
    for i in range(max_len):
        r_char = result[i] if i < len(result) else '?'
        t_char = target[i] if i < len(target) else '?'
        match = '✓' if r_char == t_char else '✗'
        print(f"  {i:2d}: '{r_char}' vs '{t_char}' {match}")
