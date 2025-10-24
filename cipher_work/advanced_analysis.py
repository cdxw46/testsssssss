#!/usr/bin/env python3

def advanced_analysis(ciphertext):
    print("=== ANÁLISIS AVANZADO ===")
    
    # Extraer solo la parte de la flag
    flag_start = ciphertext.find("34F{")
    if flag_start != -1:
        flag_end = ciphertext.find("}", flag_start)
        if flag_end != -1:
            flag_content = ciphertext[flag_start:flag_end+1]
            print(f"Flag cifrada: {flag_content}")
            
            # El formato esperado es FGTE{HURUF_BESAR_SEMUA}
            # Esto significa que 34F debería ser FGTE
            # Analicemos la correspondencia:
            # 3 -> G
            # 4 -> T  
            # F -> E
            
            # Y el contenido debería ser HURUF_BESAR_SEMUA
            flag_inner = flag_content[4:-1]
            print(f"Contenido interno: {flag_inner}")
            
            # Intentemos mapear basándonos en esta pista
            # Si 34F = FGTE, entonces:
            # 3 = G, 4 = T, F = E
            
            # Analicemos el patrón completo
            print("\n=== MAPEO BASADO EN LA FLAG ===")
            print("Si 34F = FGTE, entonces:")
            print("3 -> G")
            print("4 -> T") 
            print("F -> E")
            
            # Busquemos más patrones en el texto
            print("\n=== BÚSQUEDA DE PATRONES ===")
            
            # Buscar "F10K" al inicio - podría ser "THIS" o similar
            print("F10K al inicio - posiblemente 'THIS' o 'THAT'")
            print("Si F10K = THIS, entonces:")
            print("F -> T")
            print("1 -> H") 
            print("0 -> I")
            print("K -> S")
            
            # Verificar consistencia
            print("\n=== VERIFICACIÓN DE CONSISTENCIA ===")
            print("De la flag: F -> E")
            print("Del inicio: F -> T")
            print("¡CONTRADICCIÓN! Esto sugiere un cifrado más complejo")
            
            # Analizar si es un cifrado de Vigenère o similar
            print("\n=== ANÁLISIS DE CIFRADO COMPUESTO ===")
            print("El texto menciona 'metode klasik' y 'memodifikasinya lagi'")
            print("Esto sugiere que es un cifrado clásico modificado")
            
            # Buscar patrones de sustitución por posición
            print("\n=== ANÁLISIS POR POSICIÓN ===")
            
            # Dividir en palabras y analizar
            words = ciphertext.split()
            print("Primeras palabras:")
            for i, word in enumerate(words[:10]):
                print(f"{i}: {word}")

def try_positional_substitution(ciphertext):
    """Intenta sustitución basada en posición"""
    print("\n=== SUSTITUCIÓN POR POSICIÓN ===")
    
    # Mapeo común de teclado QWERTY
    qwerty_map = {
        'Q': 'A', 'W': 'B', 'E': 'C', 'R': 'D', 'T': 'E', 'Y': 'F', 'U': 'G', 'I': 'H', 'O': 'I', 'P': 'J',
        'A': 'K', 'S': 'L', 'D': 'M', 'F': 'N', 'G': 'O', 'H': 'P', 'J': 'Q', 'K': 'R', 'L': 'S',
        'Z': 'T', 'X': 'U', 'C': 'V', 'V': 'W', 'B': 'X', 'N': 'Y', 'M': 'Z'
    }
    
    result = ""
    for char in ciphertext:
        if char in qwerty_map:
            result += qwerty_map[char]
        else:
            result += char
    
    print("Resultado con mapeo QWERTY:")
    print(result[:300] + "..." if len(result) > 300 else result)

def try_shift_cipher(ciphertext):
    """Intenta diferentes desplazamientos"""
    print("\n=== CIFRADO DE DESPLAZAMIENTO ===")
    
    for shift in range(1, 26):
        result = ""
        for char in ciphertext:
            if 'A' <= char <= 'Z':
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            elif 'a' <= char <= 'z':
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                result += char
        
        # Buscar palabras comunes en el resultado
        if any(word in result.upper() for word in ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WAY', 'WHO', 'BOY', 'DID', 'MAN', 'MEN', 'PUT', 'SAY', 'SHE', 'TOO', 'USE']):
            print(f"Shift {shift}: {result[:200]}...")
            if 'THE' in result.upper() or 'AND' in result.upper():
                print(f"*** POSIBLE SOLUCIÓN CON SHIFT {shift} ***")

if __name__ == "__main__":
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    advanced_analysis(ciphertext)
    try_positional_substitution(ciphertext)
    try_shift_cipher(ciphertext)