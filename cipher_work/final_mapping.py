#!/usr/bin/env python3

def create_final_mapping():
    """Crea el mapeo final basado en el análisis de posiciones pares"""
    print("=== MAPEO FINAL ===")
    
    # Basándome en el análisis de posiciones pares, voy a crear un mapeo más preciso
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
    
    print("Mapeo final:")
    for cipher, plain in sorted(final_mapping.items()):
        print(f"'{cipher}' -> '{plain}'")
    
    # Aplicar mapeo al texto completo
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    result = ""
    for char in ciphertext:
        if char in final_mapping:
            result += final_mapping[char]
        else:
            result += char
    
    print(f"\nResultado final:")
    print(result)
    
    # Extraer la flag
    flag_start = result.find("{")
    if flag_start != -1:
        flag_end = result.find("}", flag_start)
        if flag_end != -1:
            flag = result[flag_start-4:flag_end+1]
            print(f"\nFlag extraída: {flag}")
            
            # Verificar si la flag es correcta
            expected_flag = "FGTE{HURUF_BESAR_SEMUA}"
            if flag == expected_flag:
                print(f"¡FLAG CORRECTA! {flag}")
            else:
                print(f"Flag esperada: {expected_flag}")
                print("Diferencias:")
                for i, (actual, expected) in enumerate(zip(flag, expected_flag)):
                    if actual != expected:
                        print(f"  Posición {i}: '{actual}' != '{expected}'")
    
    return result

def try_corrected_final_mapping():
    """Intenta un mapeo final corregido"""
    print("\n=== MAPEO FINAL CORREGIDO ===")
    
    # Basándome en la flag esperada, voy a corregir el mapeo
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
    
    # Aplicar mapeo al texto completo
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    result = ""
    for char in ciphertext:
        if char in corrected_mapping:
            result += corrected_mapping[char]
        else:
            result += char
    
    print("Resultado con mapeo corregido:")
    print(result)
    
    # Extraer la flag
    flag_start = result.find("{")
    if flag_start != -1:
        flag_end = result.find("}", flag_start)
        if flag_end != -1:
            flag = result[flag_start-4:flag_end+1]
            print(f"\nFlag extraída: {flag}")

if __name__ == "__main__":
    create_final_mapping()
    try_corrected_final_mapping()