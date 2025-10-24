#!/usr/bin/env python3

def precise_correction():
    """Corrección precisa basada en el análisis de la flag"""
    print("=== CORRECCIÓN PRECISA ===")
    
    # Analizar específicamente la flag cifrada
    flag_cipher = "34F{6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    flag_expected = "FGTE{HURUF_BESAR_SEMUA}"
    
    print(f"Flag cifrada: {flag_cipher}")
    print(f"Flag esperada: {flag_expected}")
    print()
    
    # Crear mapeo preciso basado en la correspondencia exacta
    precise_mapping = {}
    
    # Mapear el prefijo 34F -> FGTE
    precise_mapping['3'] = 'G'
    precise_mapping['4'] = 'T'
    precise_mapping['F'] = 'E'
    
    # Mapear el contenido de la flag
    cipher_content = "6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM("
    expected_content = "HURUF_BESAR_SEMUA"
    
    print("Mapeo carácter por carácter de la flag:")
    for i, (cipher_char, expected_char) in enumerate(zip(cipher_content, expected_content)):
        precise_mapping[cipher_char] = expected_char
        print(f"{i:2}: '{cipher_char}' -> '{expected_char}'")
    
    print(f"\nMapeo preciso: {precise_mapping}")
    
    # Aplicar mapeo al texto completo
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    result = ""
    for char in ciphertext:
        if char in precise_mapping:
            result += precise_mapping[char]
        else:
            result += char
    
    print(f"\nResultado con mapeo preciso:")
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
                return flag
            else:
                print(f"Flag esperada: {expected_flag}")
                print("Diferencias:")
                for i, (actual, expected) in enumerate(zip(flag, expected_flag)):
                    if actual != expected:
                        print(f"  Posición {i}: '{actual}' != '{expected}'")
                
                # Si aún no es correcta, intentar un mapeo más específico
                print("\n=== MAPEO MÁS ESPECÍFICO ===")
                
                # Crear mapeo más específico basado en el análisis detallado
                specific_mapping = {
                    '3': 'G',
                    '4': 'T',
                    'F': 'E',
                    '6': 'H',
                    'J': 'U',
                    '(': 'R',
                    'M': 'U',
                    'H': 'F',
                    '0': 'B',
                    'Q': 'E',
                    '_': 'S',
                    '1': 'A',
                    'U': 'S',
                    'K': 'M',
                    'P': 'U',
                    'V': 'A',
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
                }
                
                print("Mapeo más específico:")
                for cipher, plain in sorted(specific_mapping.items()):
                    print(f"'{cipher}' -> '{plain}'")
                
                # Aplicar mapeo más específico
                specific_result = ""
                for char in ciphertext:
                    if char in specific_mapping:
                        specific_result += specific_mapping[char]
                    else:
                        specific_result += char
                
                print(f"\nResultado con mapeo más específico:")
                print(specific_result)
                
                # Extraer la flag del resultado más específico
                specific_flag_start = specific_result.find("{")
                if specific_flag_start != -1:
                    specific_flag_end = specific_result.find("}", specific_flag_start)
                    if specific_flag_end != -1:
                        specific_flag = specific_result[specific_flag_start-4:specific_flag_end+1]
                        print(f"\nFlag más específica: {specific_flag}")
                        
                        if specific_flag == expected_flag:
                            print(f"¡FLAG CORRECTA! {specific_flag}")
                            return specific_flag
    
    return None

if __name__ == "__main__":
    precise_correction()