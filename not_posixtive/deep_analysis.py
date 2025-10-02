#!/usr/bin/env python3

def analyze_execute_function():
    """Analizar la función execute en detalle"""
    
    print("=== Análisis de la función execute ===")
    print("La función execute hace:")
    print("1. Ejecuta subprocess.run([bin, switch, compl], ...)")
    print("2. Devuelve (result.returncode * mode, partial_output)")
    print("3. Si hay excepción, devuelve (-126, 'error')")
    
    print("\n=== Análisis de check_win ===")
    print("check_win llama a execute dos veces:")
    print("1. run('{bin}', '{switches[0]}', '{args[0]}', {mode})")
    print("2. run('{bin}', '{switches[1]}', '{args[1]}', {mode})")
    
    print("\nSi cualquiera de los parámetros es falso, se ejecuta la línea aleatoria:")
    print("Línea 59: random.choice([\"This is our world now...\", 0xd3adb335, b\"HTB{\"])")
    print("Línea 66: random.choice([\"My crime is that of curiosity\", 0xd3adc0d3, b\"}BTH\"])")
    
    print("\n=== Estrategia ===")
    print("Necesitamos que ambas llamadas a execute fallen y devuelvan valores aleatorios")
    print("Pero los valores aleatorios no tienen colisiones de hash")
    print("¿Qué pasa si manipulamos el resultado de execute?")

def test_execute_manipulation():
    """Probar si podemos manipular el resultado de execute"""
    
    print("\n=== Probando manipulación de execute ===")
    
    # Simular diferentes escenarios de execute
    scenarios = [
        # Escenario 1: Comando exitoso
        (0, "OK"),
        (1, "ERR"),
        (-1, "FAIL"),
        
        # Escenario 2: Comando que falla
        (-126, "error"),
        
        # Escenario 3: Valores aleatorios cuando falla
        ("This is our world now...", "empty"),
        (0xd3adb335, "empty"),
        (b"HTB{", "empty"),
        ("My crime is that of curiosity", "empty"),
        (0xd3adc0d3, "empty"),
        (b"}BTH", "empty"),
    ]
    
    for i, (z, letter) in enumerate(scenarios):
        print(f"Escenario {i+1}: z={z}, letter={letter}")
        print(f"  Tipo de z: {type(z)}")
        print(f"  Hash de z: {hash(z)}")
        print()

def find_hash_collision_in_execute_results():
    """Buscar colisiones de hash en los resultados posibles de execute"""
    
    print("=== Buscando colisiones en resultados de execute ===")
    
    # Valores que puede devolver execute
    execute_results = [
        (0, "OK"), (1, "ERR"), (-1, "FAIL"), (-126, "error"),
        ("This is our world now...", "empty"),
        (0xd3adb335, "empty"),
        (b"HTB{", "empty"),
        ("My crime is that of curiosity", "empty"),
        (0xd3adc0d3, "empty"),
        (b"}BTH", "empty"),
    ]
    
    # Buscar colisiones entre los primeros elementos (z)
    z_values = [result[0] for result in execute_results]
    
    print("Valores z posibles:")
    for z in z_values:
        print(f"  {z} (tipo: {type(z)}, hash: {hash(z)})")
    
    print("\nBuscando colisiones:")
    hash_table = {}
    for z in z_values:
        h = hash(z)
        if h in hash_table:
            print(f"¡Colisión encontrada!")
            print(f"  {hash_table[h]} y {z} tienen hash {h}")
            print(f"  {hash_table[h]} != {z}: {hash_table[h] != z}")
            print(f"  str({hash_table[h]}) != str({z}): {str(hash_table[h]) != str(z)}")
            print(f"  isinstance({hash_table[h]}, type({z})): {isinstance(hash_table[h], type(z))}")
            return hash_table[h], z
        hash_table[h] = z
    
    print("No se encontraron colisiones automáticas")
    return None, None

def test_special_values():
    """Probar valores especiales que podrían tener colisiones"""
    
    print("\n=== Probando valores especiales ===")
    
    # Probar números que podrían tener el mismo hash
    import sys
    
    # En Python, el hash de enteros es el mismo que el valor para números pequeños
    # Pero para números grandes, se aplica módulo
    
    # Buscar dos enteros con el mismo hash
    for i in range(-1000, 1000):
        for j in range(i+1, 1000):
            if hash(i) == hash(j) and i != j:
                print(f"Colisión de enteros: {i} y {j} tienen hash {hash(i)}")
                print(f"  {i} != {j}: {i != j}")
                print(f"  str({i}) != str({j}): {str(i) != str(j)}")
                print(f"  isinstance({i}, type({j})): {isinstance(i, type(j))}")
                return i, j
    
    print("No se encontraron colisiones de enteros simples")
    return None, None

def test_float_collisions():
    """Probar colisiones con flotantes"""
    
    print("\n=== Probando colisiones de flotantes ===")
    
    # Probar flotantes que podrían tener el mismo hash
    for i in range(100):
        for j in range(i+1, 100):
            f1 = float(i)
            f2 = float(j)
            if hash(f1) == hash(f2) and f1 != f2:
                print(f"Colisión de flotantes: {f1} y {f2} tienen hash {hash(f1)}")
                return f1, f2
    
    print("No se encontraron colisiones de flotantes simples")
    return None, None

if __name__ == "__main__":
    analyze_execute_function()
    test_execute_manipulation()
    find_hash_collision_in_execute_results()
    test_special_values()
    test_float_collisions()