#!/usr/bin/env python3

def analyze_final_flag():
    """Analiza la flag final del resultado"""
    print("=== ANÁLISIS DE LA FLAG FINAL ===")
    
    # La flag final del resultado anterior es:
    final_flag = "M_PU{NHURUPSNESES_EPMUAASMSEUASRUHNRPSAUBLRU}"
    expected_flag = "FGTE{HURUF_BESAR_SEMUA}"
    
    print(f"Flag final: {final_flag}")
    print(f"Flag esperada: {expected_flag}")
    print()
    
    # Extraer contenido interno
    flag_content = "NHURUPSNESES_EPMUAASMSEUASRUHNRPSAUBLRU"
    expected_content = "HURUF_BESAR_SEMUA"
    
    print(f"Contenido: {flag_content}")
    print(f"Esperado: {expected_content}")
    print()
    
    # Analizar carácter por carácter
    print("Análisis carácter por carácter:")
    for i, (cipher_char, expected_char) in enumerate(zip(flag_content, expected_content)):
        print(f"{i:2}: '{cipher_char}' -> '{expected_char}'")
    
    # Buscar patrones
    print("\n=== BÚSQUEDA DE PATRONES ===")
    
    # Buscar si hay caracteres que se repiten incorrectamente
    print("Caracteres únicos en el contenido:")
    unique_chars = set(flag_content)
    print(sorted(unique_chars))
    
    # Buscar si hay un patrón de duplicación
    print("\nBuscando patrones de duplicación:")
    for i in range(len(flag_content) - 1):
        if flag_content[i] == flag_content[i + 1]:
            print(f"Duplicación en posición {i}: '{flag_content[i]}{flag_content[i+1]}'")

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
    
    # Aplicar el mapeo al texto original
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    result = ""
    for char in ciphertext:
        if char in corrected_mapping:
            result += corrected_mapping[char]
        else:
            result += char
    
    print("Resultado con mapeo corregido:")
    print(result)
    
    # Extraer solo la flag
    flag_start = result.find("{")
    if flag_start != -1:
        flag_end = result.find("}", flag_start)
        if flag_end != -1:
            flag = result[flag_start-4:flag_end+1]
            print(f"\nFlag extraída: {flag}")

def try_alternative_approach():
    """Intenta un enfoque alternativo"""
    print("\n=== ENFOQUE ALTERNATIVO ===")
    
    # Tal vez el cifrado no es una sustitución simple
    # Voy a intentar analizar si es un cifrado de Vigenère con clave específica
    
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    # Intentar con diferentes claves de Vigenère
    possible_keys = ['FGTE', 'FLAG', 'CTF', 'CRYPTO', 'INDONESIA', 'CIPHER', 'PESAN']
    
    for key in possible_keys:
        result = vigenere_decrypt(ciphertext, key)
        print(f"\nClave '{key}':")
        print(result[:200] + "..." if len(result) > 200 else result)
        
        # Buscar la flag en el resultado
        if 'FGTE{' in result or 'HURUF' in result:
            print(f"*** POSIBLE SOLUCIÓN CON CLAVE '{key}' ***")
            flag_start = result.find('{')
            if flag_start != -1:
                flag_end = result.find('}', flag_start)
                if flag_end != -1:
                    flag = result[flag_start-4:flag_end+1]
                    print(f"Flag: {flag}")

def vigenere_decrypt(ciphertext, key):
    """Descifra con Vigenère"""
    result = ""
    key_index = 0
    
    for char in ciphertext:
        if 'A' <= char <= 'Z':
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            key_index += 1
        else:
            result += char
    
    return result

if __name__ == "__main__":
    analyze_final_flag()
    try_corrected_mapping()
    try_alternative_approach()