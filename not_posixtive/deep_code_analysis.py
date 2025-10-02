#!/usr/bin/env python3

def deep_analysis():
    """Análisis profundo del código para encontrar otras vulnerabilidades"""
    
    print("=== ANÁLISIS PROFUNDO DEL CÓDIGO ===")
    
    print("\n1. Función execute:")
    print("   - Ejecuta: subprocess.run([bin, switch, compl], ...)")
    print("   - Devuelve: (result.returncode * mode, partial_output)")
    print("   - Si excepción: (-126, 'error')")
    
    print("\n2. Función check_win:")
    print("   - Llama a execute dos veces")
    print("   - Si parámetros son falsos, usa valores aleatorios")
    print("   - Condición: debug[0] != debug[1] AND str(debug[0]) != str(debug[1]) AND hash(debug[0]) == hash(debug[1]) AND isinstance(debug[0], type(debug[1]))")
    
    print("\n3. Función eval:")
    print("   - Se usa en líneas 57 y 64: eval(f\"run('{bin}', '{switches[0]}', '{args[0]}', {mode})\", globs, locs)")
    print("   - globs = {\"__builtins__\": {}, \"run\": execute}")
    print("   - locs = {}")
    
    print("\n4. POSIBLE VULNERABILIDAD: eval()")
    print("   - El eval() ejecuta código Python")
    print("   - Aunque __builtins__ está vacío, podría haber formas de explotarlo")
    print("   - Los parámetros se insertan directamente en la cadena eval")
    
    print("\n5. ANÁLISIS DE LA CADENA eval:")
    print("   - f\"run('{bin}', '{switches[0]}', '{args[0]}', {mode})\"")
    print("   - bin, switches[0], args[0] están entre comillas simples")
    print("   - mode no está entre comillas")
    print("   - Esto significa que mode se evalúa como código Python")
    
    print("\n6. VULNERABILIDAD EN mode:")
    print("   - mode se evalúa como código Python")
    print("   - Si mode contiene código malicioso, se ejecutará")
    print("   - Pero check_operands() limita lo que puede ser mode")
    
    print("\n7. ANÁLISIS DE check_operands:")
    print("   - Toma los primeros 2 caracteres")
    print("   - Si contiene operadores, devuelve 0")
    print("   - Si no, evalúa la expresión")
    print("   - Esto significa que podemos usar expresiones Python simples")

def test_mode_evaluation():
    """Probar qué se puede hacer con mode"""
    
    print("\n=== PROBANDO EVALUACIÓN DE mode ===")
    
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
    
    # Probar diferentes valores para mode
    test_values = [
        "1",      # 1
        "2",      # 2
        "3",      # 3
        "4",      # 4
        "5",      # 5
        "10",     # 10
        "42",     # 42
        "0",      # 0
        "True",   # True
        "False",  # False
        "None",   # None
    ]
    
    for value in test_values:
        result = check_operands(value)
        print(f"check_operands('{value}') = {result} (tipo: {type(result)})")

def analyze_eval_string_construction():
    """Analizar cómo se construye la cadena eval"""
    
    print("\n=== ANÁLISIS DE CONSTRUCCIÓN DE CADENA eval ===")
    
    # Simular diferentes valores
    bin_val = "ls"
    switch_val = "a"
    arg_val = "b"
    mode_val = 1
    
    eval_string = f"run('{bin_val}', '{switch_val}', '{arg_val}', {mode_val})"
    print(f"Cadena eval: {eval_string}")
    
    # ¿Qué pasa si mode es un objeto especial?
    print("\nProbando mode especiales:")
    
    # Si mode es una función que devuelve objetos con colisión de hash
    class CollisionMaker:
        def __init__(self):
            self.call_count = 0
        
        def __call__(self):
            self.call_count += 1
            if self.call_count == 1:
                return -2  # Primer resultado
            else:
                return -1  # Segundo resultado
        
        def __int__(self):
            return self()
    
    # Probar si podemos usar esto
    print("¿Podemos usar objetos personalizados como mode?")

def find_alternative_vulnerabilities():
    """Buscar otras vulnerabilidades en el código"""
    
    print("\n=== BUSCANDO OTRAS VULNERABILIDADES ===")
    
    print("1. VULNERABILIDAD EN eval():")
    print("   - Los parámetros se insertan directamente en eval")
    print("   - Aunque __builtins__ está vacío, podría haber escapes")
    
    print("2. VULNERABILIDAD EN subprocess.run():")
    print("   - Se ejecuta con [bin, switch, compl]")
    print("   - Si podemos controlar estos parámetros de forma inesperada...")
    
    print("3. VULNERABILIDAD EN CONDICIÓN DE VICTORIA:")
    print("   - La condición requiere colisión de hash")
    print("   - Pero tal vez podemos manipular los valores de otra manera")
    
    print("4. VULNERABILIDAD EN VALIDACIONES:")
    print("   - Las validaciones son estrictas")
    print("   - Pero tal vez hay formas de bypasearlas")
    
    print("5. VULNERABILIDAD EN GLOBALS/LOCALS:")
    print("   - globs = {\"__builtins__\": {}, \"run\": execute}")
    print("   - locs = {}")
    print("   - Tal vez podemos modificar estos")

def test_eval_escape():
    """Probar si podemos escapar del eval"""
    
    print("\n=== PROBANDO ESCAPE DE eval ===")
    
    # Simular el entorno eval
    def execute(bin, switch, compl, mode):
        print(f"execute llamado con: bin='{bin}', switch='{switch}', compl='{compl}', mode={mode}")
        return (0, "test")
    
    globs = {
        "__builtins__": {},
        "run": execute
    }
    locs = {}
    
    # Probar diferentes formas de escapar
    test_cases = [
        "run('ls', 'a', 'b', 1)",
        "run('ls', 'a', 'b', 1) # comentario",
        "run('ls', 'a', 'b', 1); print('escape')",
        "run('ls', 'a', 'b', 1)\nprint('escape')",
    ]
    
    for test_case in test_cases:
        try:
            print(f"Probando: {test_case}")
            result = eval(test_case, globs, locs)
            print(f"Resultado: {result}")
        except Exception as e:
            print(f"Error: {e}")
        print()

if __name__ == "__main__":
    deep_analysis()
    test_mode_evaluation()
    analyze_eval_string_construction()
    find_alternative_vulnerabilities()
    test_eval_escape()