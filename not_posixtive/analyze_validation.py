#!/usr/bin/env python3

def analyze_validation_functions():
    """Analizar las funciones de validación del servidor"""
    
    print("=== Análisis de funciones de validación ===")
    
    print("\n1. check_stricter_values(value):")
    print("   - Toma los primeros 4 caracteres después de strip")
    print("   - Solo permite caracteres alfabéticos y puntos")
    print("   - Se usa para 'bin'")
    
    print("\n2. check_values(value):")
    print("   - Toma los primeros 13 caracteres después de strip")
    print("   - Solo permite caracteres alfabéticos y puntos")
    print("   - Se usa para 'args' y 'switches'")
    
    print("\n3. check_operands(value):")
    print("   - Toma los primeros 2 caracteres después de strip")
    print("   - Si contiene operadores ['+', '-', '*', '/', '%', '=', 'x', 'o', 'b'], devuelve 0")
    print("   - Si no, evalúa la expresión y devuelve el resultado")
    print("   - Se usa para 'mode'")
    
    print("\n=== Problemas identificados ===")
    print("1. Los comandos fallan porque las validaciones son muy estrictas")
    print("2. 'bin' solo puede tener 4 caracteres alfabéticos")
    print("3. 'args' y 'switches' solo pueden tener caracteres alfabéticos")
    print("4. Esto limita severamente qué comandos podemos ejecutar")

def test_validation_functions():
    """Probar las funciones de validación"""
    
    print("\n=== Probando validaciones ===")
    
    # Simular check_stricter_values
    def check_stricter_values(value):
        s = value.lstrip().strip()[:4]
        if not s:
            return ""
        for char in s:
            if not (char.isalpha() or char == '.'): 
                return ""
        return s
    
    # Simular check_values
    def check_values(value):
        s = value.lstrip().strip()[:13]
        if not s:
            return ""
        for char in s:
            if not (char.isalpha() or char == '.'): 
                return ""
        return s
    
    # Simular check_operands
    def check_operands(value):
        s = value.lstrip().strip()[:2]
        operators = ['+', '-', '*', '/', '%', '=', 'x', 'o', 'b']
        
        if any(op in s for op in operators):
            return 0
        else:
            try:
                evaluated = eval(s)
                return evaluated
            except Exception as e:
                return 0
    
    # Probar diferentes valores
    test_cases = [
        ("ls", check_stricter_values),
        ("python3", check_stricter_values),
        ("pyth", check_stricter_values),
        ("exit(2)", check_values),
        ("/nonexistent", check_values),
        ("-la", check_values),
        ("-c", check_values),
        ("-1", check_operands),
        ("1", check_operands),
        ("2", check_operands),
    ]
    
    for value, func in test_cases:
        result = func(value)
        print(f"{func.__name__}('{value}') = '{result}'")

def find_valid_commands():
    """Encontrar comandos válidos que podamos usar"""
    
    print("\n=== Buscando comandos válidos ===")
    
    def check_stricter_values(value):
        s = value.lstrip().strip()[:4]
        if not s:
            return ""
        for char in s:
            if not (char.isalpha() or char == '.'): 
                return ""
        return s
    
    def check_values(value):
        s = value.lstrip().strip()[:13]
        if not s:
            return ""
        for char in s:
            if not (char.isalpha() or char == '.'): 
                return ""
        return s
    
    # Comandos válidos para 'bin' (4 caracteres, solo letras)
    valid_bins = []
    for cmd in ["ls", "cat", "pwd", "who", "id", "ps", "df", "du", "wc", "od", "xxd", "hexdump"]:
        if len(cmd) <= 4:
            result = check_stricter_values(cmd)
            if result:
                valid_bins.append(result)
    
    print(f"Comandos válidos para 'bin': {valid_bins}")
    
    # Argumentos válidos (solo letras)
    valid_args = []
    for arg in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]:
        result = check_values(arg)
        if result:
            valid_args.append(result)
    
    print(f"Argumentos válidos: {valid_args}")
    
    # Switches válidos (solo letras)
    valid_switches = []
    for switch in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]:
        result = check_values(switch)
        if result:
            valid_switches.append(result)
    
    print(f"Switches válidos: {valid_switches}")

def analyze_why_commands_fail():
    """Analizar por qué los comandos fallan"""
    
    print("\n=== Análisis de por qué fallan los comandos ===")
    
    print("Los comandos fallan porque:")
    print("1. Las validaciones son muy estrictas")
    print("2. No podemos usar caracteres especiales como '-', '/', números")
    print("3. Esto significa que no podemos usar la mayoría de comandos del sistema")
    
    print("\nPosibles soluciones:")
    print("1. Usar comandos que no requieran argumentos especiales")
    print("2. Hacer que los comandos fallen intencionalmente para obtener valores aleatorios")
    print("3. Buscar comandos que devuelvan códigos de error específicos")
    
    print("\nEstrategia alternativa:")
    print("Si no podemos hacer que los comandos se ejecuten correctamente,")
    print("tal vez podemos hacer que fallen de manera controlada para obtener")
    print("valores aleatorios que cumplan la condición de hash collision")

if __name__ == "__main__":
    analyze_validation_functions()
    test_validation_functions()
    find_valid_commands()
    analyze_why_commands_fail()