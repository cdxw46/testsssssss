#!/usr/bin/env python3

def create_refined_mapping():
    """Crea un mapeo refinado basado en el análisis de la flag"""
    print("=== MAPEO REFINADO ===")
    
    # Del análisis anterior, tenemos estas correspondencias de la flag:
    flag_mapping = {
        '6': '{',  # o podría ser otra cosa
        'J': 'H',
        '(': 'U', 
        'M': 'R',
        'H': 'U',
        'F': 'F',
        '0': '_',
        'Q': 'E',
        '_': 'S',
        '4': '_',
        '1': 'S',
        '3': 'M',
        'U': 'A'
    }
    
    print("Mapeo de la flag:")
    for cipher, plain in flag_mapping.items():
        print(f"'{cipher}' -> '{plain}'")
    
    # Aplicar el mapeo al texto completo
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    result = ""
    for char in ciphertext:
        if char in flag_mapping:
            result += flag_mapping[char]
        else:
            result += char
    
    print(f"\nResultado con mapeo de la flag:")
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Buscar palabras indonesias en el resultado
    print("\n=== BÚSQUEDA DE PALABRAS INDONESIAS ===")
    indonesian_words = ['DAN', 'UNTUK', 'YANG', 'INI', 'ADALAH', 'DARI', 'PADA', 'TETAPI', 'SEPERTINYA']
    
    for word in indonesian_words:
        if word in result.upper():
            print(f"Encontrada palabra indonesia: {word}")
    
    return result, flag_mapping

def try_complete_mapping():
    """Intenta completar el mapeo con más caracteres"""
    print("\n=== COMPLETANDO EL MAPEO ===")
    
    # Mapeo base de la flag
    base_mapping = {
        'J': 'H',
        '(': 'U', 
        'M': 'R',
        'H': 'U',
        'F': 'F',
        '0': '_',
        'Q': 'E',
        '_': 'S',
        '4': '_',
        '1': 'S',
        '3': 'M',
        'U': 'A'
    }
    
    # Analizar el texto para encontrar más correspondencias
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    # Aplicar mapeo base
    partial_result = ""
    for char in ciphertext:
        if char in base_mapping:
            partial_result += base_mapping[char]
        else:
            partial_result += char
    
    print("Resultado parcial:")
    print(partial_result[:300] + "..." if len(partial_result) > 300 else partial_result)
    
    # Buscar patrones en el resultado parcial
    print("\n=== ANÁLISIS DEL RESULTADO PARCIAL ===")
    
    # Buscar palabras que podrían ser "PESAN" (mensaje en indonesio)
    # Si "F10K" fuera "PESAN", entonces:
    # F -> P, 1 -> E, 0 -> S, K -> A, N
    
    print("Si F10K = PESAN, entonces:")
    print("F -> P")
    print("1 -> E") 
    print("0 -> S")
    print("K -> A")
    
    # Crear mapeo extendido
    extended_mapping = base_mapping.copy()
    extended_mapping.update({
        'F': 'P',  # Sobrescribir F -> F con F -> P
        '1': 'E',  # Sobrescribir 1 -> S con 1 -> E
        '0': 'S',  # Sobrescribir 0 -> _ con 0 -> S
        'K': 'A'   # Nuevo
    })
    
    print(f"\nMapeo extendido: {extended_mapping}")
    
    # Aplicar mapeo extendido
    extended_result = ""
    for char in ciphertext:
        if char in extended_mapping:
            extended_result += extended_mapping[char]
        else:
            extended_result += char
    
    print(f"\nResultado con mapeo extendido:")
    print(extended_result[:400] + "..." if len(extended_result) > 400 else extended_result)
    
    return extended_result, extended_mapping

def try_final_decryption():
    """Intenta la descifrado final"""
    print("\n=== DESCIFRADO FINAL ===")
    
    # Basándome en el análisis, voy a crear un mapeo más completo
    final_mapping = {
        'F': 'P',
        '1': 'E', 
        '0': 'S',
        'K': 'A',
        'J': 'H',
        '(': 'U',
        'M': 'R', 
        'H': 'U',
        'Q': 'E',
        '_': 'S',
        '4': '_',
        '3': 'M',
        'U': 'A',
        '6': 'N',  # Posible
        'Y': 'D',  # Posible
        'P': 'B',  # Posible
        'D': 'I',  # Posible
        'V': 'L',  # Posible
        '5': 'G',  # Posible
        'R': 'T',  # Posible
        '2': 'C',  # Posible
        'L': 'Y',  # Posible
        'W': 'W',  # Posible
        'N': 'N',  # Posible
        'T': 'T',  # Posible
        ';': ';',
        ',': ',',
        '.': '.',
        ' ': ' ',
        '{': '{',
        '}': '}'
    }
    
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    result = ""
    for char in ciphertext:
        if char in final_mapping:
            result += final_mapping[char]
        else:
            result += char
    
    print("Resultado final:")
    print(result)
    
    return result

if __name__ == "__main__":
    create_refined_mapping()
    try_complete_mapping()
    try_final_decryption()