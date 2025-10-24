#!/usr/bin/env python3

def analyze_patterns():
    """Analiza patrones en el cifrado"""
    print("=== ANÁLISIS DE PATRONES ===")
    
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    # Analizar la flag específicamente
    flag_part = "34F{6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    expected_flag = "FGTE{HURUF_BESAR_SEMUA}"
    
    print(f"Flag cifrada: {flag_part}")
    print(f"Flag esperada: {expected_flag}")
    print()
    
    # Extraer contenido interno
    flag_content = "6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM("
    expected_content = "HURUF_BESAR_SEMUA"
    
    print(f"Contenido cifrado: {flag_content}")
    print(f"Contenido esperado: {expected_content}")
    print()
    
    # Analizar si hay caracteres de relleno
    print("=== ANÁLISIS DE CARACTERES DE RELLENO ===")
    
    # Buscar patrones de repetición
    print("Buscando patrones de repetición:")
    for i in range(len(flag_content) - 1):
        if flag_content[i] == flag_content[i + 1]:
            print(f"Repetición en posición {i}: '{flag_content[i]}{flag_content[i+1]}'")
    
    # Analizar si hay un patrón de intercalado
    print("\n=== ANÁLISIS DE INTERCALADO ===")
    
    # Intentar extraer caracteres en posiciones pares e impares
    even_chars = flag_content[::2]  # Posiciones pares (0, 2, 4, ...)
    odd_chars = flag_content[1::2]  # Posiciones impares (1, 3, 5, ...)
    
    print(f"Caracteres en posiciones pares: {even_chars}")
    print(f"Caracteres en posiciones impares: {odd_chars}")
    print(f"Longitud par: {len(even_chars)}, Longitud impar: {len(odd_chars)}")
    
    # Verificar si alguno coincide con el contenido esperado
    if len(even_chars) == len(expected_content):
        print(f"¿Posiciones pares coinciden? {even_chars == expected_content}")
    
    if len(odd_chars) == len(expected_content):
        print(f"¿Posiciones impares coinciden? {odd_chars == expected_content}")
    
    # Intentar mapeo directo de posiciones pares
    if len(even_chars) == len(expected_content):
        print("\n=== MAPEO DE POSICIONES PARES ===")
        for i, (cipher_char, expected_char) in enumerate(zip(even_chars, expected_content)):
            print(f"{i:2}: '{cipher_char}' -> '{expected_char}'")

def try_positional_mapping():
    """Intenta mapeo basado en posición"""
    print("\n=== MAPEO BASADO EN POSICIÓN ===")
    
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    # Crear mapeo basado en posiciones pares de la flag
    flag_mapping = {
        '6': 'H',
        'J': 'U', 
        'M': 'R',
        'H': 'U',
        'F': 'F',
        '0': '_',
        'Q': 'B',
        '_': 'E',
        '4': 'S',
        '1': 'A',
        '3': 'R',
        'U': 'S',
        'K': 'E',
        'P': 'M',
        'V': 'U',
        '(': 'A'
    }
    
    print("Mapeo basado en posiciones pares:")
    for cipher, plain in flag_mapping.items():
        print(f"'{cipher}' -> '{plain}'")
    
    # Aplicar mapeo al texto completo
    result = ""
    for char in ciphertext:
        if char in flag_mapping:
            result += flag_mapping[char]
        else:
            result += char
    
    print(f"\nResultado con mapeo de posiciones pares:")
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Extraer la flag
    flag_start = result.find("{")
    if flag_start != -1:
        flag_end = result.find("}", flag_start)
        if flag_end != -1:
            flag = result[flag_start-4:flag_end+1]
            print(f"\nFlag extraída: {flag}")

def try_alternating_pattern():
    """Intenta patrón alternante"""
    print("\n=== PATRÓN ALTERNANTE ===")
    
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    # Intentar extraer solo caracteres en posiciones específicas
    # Basándome en el análisis anterior, voy a intentar diferentes patrones
    
    # Patrón 1: Cada segundo carácter
    pattern1 = ciphertext[::2]
    print(f"Patrón 1 (cada 2do carácter): {pattern1[:100]}...")
    
    # Patrón 2: Cada tercer carácter
    pattern2 = ciphertext[::3]
    print(f"Patrón 2 (cada 3er carácter): {pattern2[:100]}...")
    
    # Patrón 3: Saltar caracteres específicos
    # Intentar ignorar paréntesis y números
    filtered = ""
    for char in ciphertext:
        if char.isalpha():
            filtered += char
    
    print(f"Patrón 3 (solo letras): {filtered[:100]}...")
    
    # Buscar si alguno de estos patrones contiene palabras indonesias
    indonesian_words = ['PESAN', 'DAN', 'UNTUK', 'YANG', 'INI', 'ADALAH']
    
    for i, pattern in enumerate([pattern1, pattern2, filtered], 1):
        print(f"\nPatrón {i}:")
        for word in indonesian_words:
            if word in pattern.upper():
                print(f"  Encontrada palabra: {word}")

if __name__ == "__main__":
    analyze_patterns()
    try_positional_mapping()
    try_alternating_pattern()