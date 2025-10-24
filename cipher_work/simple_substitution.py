#!/usr/bin/env python3

def simple_substitution_analysis():
    """Análisis de sustitución simple"""
    print("=== ANÁLISIS DE SUSTITUCIÓN SIMPLE ===")
    
    # Flag cifrada y esperada
    cipher_flag = "34F{6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    expected_flag = "FGTE{HURUF_BESAR_SEMUA}"
    
    print(f"Flag cifrada: {cipher_flag}")
    print(f"Flag esperada: {expected_flag}")
    print()
    
    # Crear mapeo directo basado en la flag
    # 34F = FGTE
    # 6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM( = HURUF_BESAR_SEMUA
    
    # Mapeo del prefijo
    prefix_mapping = {
        '3': 'G',
        '4': 'T',
        'F': 'E'
    }
    
    # Mapeo del contenido
    content_mapping = {
        '6': 'H',
        'J': 'U',
        '(': 'R',
        'M': 'U',
        'H': 'F',
        'F': '_',
        '0': 'B',
        'Q': 'E',
        '_': 'S',
        '4': 'A',
        '1': 'R',
        '3': 'S',
        'U': 'E',
        'K': 'M',
        'P': 'U',
        'V': 'A'
    }
    
    # Combinar mapeos
    full_mapping = {**prefix_mapping, **content_mapping}
    
    print("Mapeo completo:")
    for cipher, plain in sorted(full_mapping.items()):
        print(f"'{cipher}' -> '{plain}'")
    
    # Aplicar mapeo al texto completo
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    result = ""
    for char in ciphertext:
        if char in full_mapping:
            result += full_mapping[char]
        else:
            result += char
    
    print(f"\nResultado:")
    print(result)
    
    # Extraer la flag
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
                print("Diferencias:")
                for i, (actual, expected) in enumerate(zip(flag, expected_flag)):
                    if actual != expected:
                        print(f"  Posición {i}: '{actual}' != '{expected}'")

def try_corrected_mapping():
    """Intenta un mapeo corregido"""
    print("\n=== MAPEO CORREGIDO ===")
    
    # Basándome en el análisis, voy a crear un mapeo más preciso
    corrected_mapping = {
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
        '6': 'N',
        'Y': 'D',
        'P': 'B',
        'D': 'I',
        'V': 'L',
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
    }
    
    print("Mapeo corregido:")
    for cipher, plain in sorted(corrected_mapping.items()):
        print(f"'{cipher}' -> '{plain}'")
    
    # Aplicar mapeo al texto completo
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    result = ""
    for char in ciphertext:
        if char in corrected_mapping:
            result += corrected_mapping[char]
        else:
            result += char
    
    print(f"\nResultado:")
    print(result)
    
    # Extraer la flag
    flag_start = result.find("{")
    if flag_start != -1:
        flag_end = result.find("}", flag_start)
        if flag_end != -1:
            flag = result[flag_start-4:flag_end+1]
            print(f"\nFlag extraída: {flag}")

if __name__ == "__main__":
    simple_substitution_analysis()
    try_corrected_mapping()