#!/usr/bin/env python3

def try_alternating_decryption():
    """Intenta descifrado alternante"""
    print("=== DESCIFRADO ALTERNANTE ===")
    
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    # Intentar extraer solo caracteres en posiciones específicas
    # Basándome en el análisis anterior, voy a intentar diferentes patrones
    
    # Patrón 1: Ignorar paréntesis y números, solo letras
    letters_only = ""
    for char in ciphertext:
        if char.isalpha():
            letters_only += char
    
    print(f"Solo letras: {letters_only[:100]}...")
    
    # Patrón 2: Ignorar números, mantener letras y símbolos
    no_numbers = ""
    for char in ciphertext:
        if not char.isdigit():
            no_numbers += char
    
    print(f"Sin números: {no_numbers[:100]}...")
    
    # Patrón 3: Solo caracteres alfanuméricos
    alphanumeric_only = ""
    for char in ciphertext:
        if char.isalnum():
            alphanumeric_only += char
    
    print(f"Solo alfanuméricos: {alphanumeric_only[:100]}...")
    
    # Buscar patrones en estos resultados
    print("\n=== BÚSQUEDA DE PATRONES ===")
    
    # Buscar palabras indonesias comunes
    indonesian_words = ['PESAN', 'DAN', 'UNTUK', 'YANG', 'INI', 'ADALAH', 'DARI', 'PADA']
    
    for i, text in enumerate([letters_only, no_numbers, alphanumeric_only], 1):
        print(f"\nPatrón {i}:")
        for word in indonesian_words:
            if word in text.upper():
                print(f"  Encontrada: {word}")

def try_vigenere_with_different_keys():
    """Intenta Vigenère con diferentes claves"""
    print("\n=== VIGENÈRE CON DIFERENTES CLAVES ===")
    
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    # Claves posibles basadas en el contexto
    possible_keys = ['FGTE', 'FLAG', 'CTF', 'CRYPTO', 'INDONESIA', 'CIPHER', 'PESAN', 'MESSAGE', 'ENCRYPT', 'DECRYPT']
    
    for key in possible_keys:
        result = vigenere_decrypt(ciphertext, key)
        print(f"\nClave '{key}':")
        print(result[:150] + "..." if len(result) > 150 else result)
        
        # Buscar la flag en el resultado
        if 'FGTE{' in result or 'HURUF' in result or 'PESAN' in result:
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

def try_caesar_with_different_shifts():
    """Intenta Caesar con diferentes desplazamientos"""
    print("\n=== CAESAR CON DIFERENTES DESPLAZAMIENTOS ===")
    
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    for shift in range(1, 26):
        result = caesar_decrypt(ciphertext, shift)
        
        # Buscar palabras indonesias en el resultado
        if any(word in result.upper() for word in ['PESAN', 'DAN', 'UNTUK', 'YANG', 'INI', 'ADALAH']):
            print(f"Shift {shift}: {result[:150]}...")
            if 'PESAN' in result.upper() or 'HURUF' in result.upper():
                print(f"*** POSIBLE SOLUCIÓN CON SHIFT {shift} ***")
                flag_start = result.find('{')
                if flag_start != -1:
                    flag_end = result.find('}', flag_start)
                    if flag_end != -1:
                        flag = result[flag_start-4:flag_end+1]
                        print(f"Flag: {flag}")

def caesar_decrypt(ciphertext, shift):
    """Descifra con Caesar"""
    result = ""
    for char in ciphertext:
        if 'A' <= char <= 'Z':
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        elif 'a' <= char <= 'z':
            result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char
    return result

if __name__ == "__main__":
    try_alternating_decryption()
    try_vigenere_with_different_keys()
    try_caesar_with_different_shifts()