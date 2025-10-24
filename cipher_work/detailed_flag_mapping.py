#!/usr/bin/env python3

def detailed_flag_mapping():
    """Mapeo detallado de la flag"""
    print("=== MAPEO DETALLADO DE LA FLAG ===")
    
    # Flag cifrada y esperada
    cipher_flag = "34F{6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    expected_flag = "FGTE{HURUF_BESAR_SEMUA}"
    
    print(f"Flag cifrada: {cipher_flag}")
    print(f"Flag esperada: {expected_flag}")
    print()
    
    # Extraer contenido interno
    cipher_content = "6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM("
    expected_content = "HURUF_BESAR_SEMUA"
    
    print(f"Contenido cifrado: {cipher_content}")
    print(f"Contenido esperado: {expected_content}")
    print()
    
    # Analizar carácter por carácter
    print("Análisis carácter por carácter:")
    print("Pos | Cifrado | Esperado | Mapeo")
    print("----|---------|----------|------")
    
    for i, (cipher_char, expected_char) in enumerate(zip(cipher_content, expected_content)):
        print(f"{i:3} |   '{cipher_char}'    |    '{expected_char}'    | {cipher_char} -> {expected_char}")
    
    # Crear mapeo basado en esta correspondencia
    flag_mapping = {}
    for cipher_char, expected_char in zip(cipher_content, expected_content):
        if cipher_char not in flag_mapping:
            flag_mapping[cipher_char] = expected_char
    
    print(f"\nMapeo de la flag: {flag_mapping}")
    
    # Aplicar mapeo al texto completo
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    result = ""
    for char in ciphertext:
        if char in flag_mapping:
            result += flag_mapping[char]
        else:
            result += char
    
    print(f"\nResultado con mapeo de la flag:")
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Extraer la flag del resultado
    flag_start = result.find("{")
    if flag_start != -1:
        flag_end = result.find("}", flag_start)
        if flag_end != -1:
            flag = result[flag_start-4:flag_end+1]
            print(f"\nFlag extraída: {flag}")
            
            if flag == expected_flag:
                print("¡FLAG CORRECTA!")
            else:
                print(f"Flag esperada: {expected_flag}")
    
    return result, flag_mapping

def try_complete_mapping():
    """Intenta completar el mapeo con más caracteres"""
    print("\n=== COMPLETANDO EL MAPEO ===")
    
    # Mapeo base de la flag
    base_mapping = {
        '6': 'H',
        'J': 'U',
        '(': 'U',
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
        'A': 'A'
    }
    
    # Agregar mapeos adicionales basados en el análisis del texto
    extended_mapping = base_mapping.copy()
    extended_mapping.update({
        'Y': 'D',
        'D': 'I',
        '5': 'G',
        'R': 'T',
        '2': 'C',
        'L': 'Y',
        'W': 'W',
        'N': 'N',
        'T': 'T',
        ';': ';',
        ',': ',',
        '.': '.',
        ' ': ' ',
        '{': '{',
        '}': '}'
    })
    
    print("Mapeo extendido:")
    for cipher, plain in sorted(extended_mapping.items()):
        print(f"'{cipher}' -> '{plain}'")
    
    # Aplicar mapeo extendido
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    result = ""
    for char in ciphertext:
        if char in extended_mapping:
            result += extended_mapping[char]
        else:
            result += char
    
    print(f"\nResultado con mapeo extendido:")
    print(result)
    
    # Extraer la flag
    flag_start = result.find("{")
    if flag_start != -1:
        flag_end = result.find("}", flag_start)
        if flag_end != -1:
            flag = result[flag_start-4:flag_end+1]
            print(f"\nFlag extraída: {flag}")

if __name__ == "__main__":
    detailed_flag_mapping()
    try_complete_mapping()