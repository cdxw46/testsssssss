#!/usr/bin/env python3

def analyze_indonesian_patterns(ciphertext):
    """Analiza patrones específicos para texto indonesio"""
    print("=== ANÁLISIS PARA TEXTO INDONESIO ===")
    
    # Palabras comunes en indonesio que podrían aparecer
    indonesian_common = [
        'DAN', 'DENGAN', 'UNTUK', 'YANG', 'INI', 'ADALAH', 'DARI', 'PADA', 
        'TIDAK', 'AKAN', 'SUDAH', 'BISA', 'HARUS', 'JIKA', 'KARENA', 'SERTA',
        'DALAM', 'DENGAN', 'UNTUK', 'YANG', 'INI', 'ADALAH', 'DARI', 'PADA',
        'TETAPI', 'SEPERTINYA', 'SESEORANG', 'MEMODIFIKASINYA', 'LAGI', 'CARA',
        'TIDAK', 'BIASA', 'PESAN', 'SUDAH', 'DIENKRIPSI', 'METODE', 'KLASIK'
    ]
    
    # Intentar diferentes mapeos basados en la flag
    # Si 34F = FGTE, entonces tenemos algunas correspondencias
    print("=== MAPEO BASADO EN ANÁLISIS DE LA FLAG ===")
    
    # Analicemos la flag más cuidadosamente
    flag_part = "34F{6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    print(f"Flag cifrada: {flag_part}")
    
    # El formato esperado es FGTE{HURUF_BESAR_SEMUA}
    # Esto nos da: 34F = FGTE
    # Y el contenido: 6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM( = HURUF_BESAR_SEMUA
    
    print("\n=== CORRESPONDENCIAS DE LA FLAG ===")
    print("34F = FGTE")
    print("6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM( = HURUF_BESAR_SEMUA")
    
    # Crear mapeo parcial
    mapping = {}
    mapping['3'] = 'G'
    mapping['4'] = 'T' 
    mapping['F'] = 'E'
    
    # Analizar el contenido de la flag
    flag_content = "6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM("
    expected = "HURUF_BESAR_SEMUA"
    
    print(f"\nContenido cifrado: {flag_content}")
    print(f"Contenido esperado: {expected}")
    print(f"Longitudes: {len(flag_content)} vs {len(expected)}")
    
    # Intentar mapear carácter por carácter
    if len(flag_content) == len(expected):
        print("\n=== MAPEO CARÁCTER POR CARÁCTER ===")
        for i, (cipher_char, plain_char) in enumerate(zip(flag_content, expected)):
            if cipher_char not in mapping:
                mapping[cipher_char] = plain_char
            print(f"{cipher_char} -> {plain_char}")
    
    print(f"\nMapeo parcial: {mapping}")
    
    # Aplicar el mapeo al texto completo
    result = ""
    for char in ciphertext:
        if char in mapping:
            result += mapping[char]
        else:
            result += char
    
    print(f"\nResultado con mapeo parcial:")
    print(result[:400] + "..." if len(result) > 400 else result)

def try_vigenere_decrypt(ciphertext, key):
    """Intenta descifrar con Vigenère"""
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

def try_vigenere_analysis(ciphertext):
    """Analiza posibles claves de Vigenère"""
    print("\n=== ANÁLISIS VIGENÈRE ===")
    
    # Claves posibles basadas en el contexto
    possible_keys = ['FGTE', 'FLAG', 'CTF', 'CRYPTO', 'INDONESIA', 'CIPHER']
    
    for key in possible_keys:
        result = try_vigenere_decrypt(ciphertext, key)
        print(f"\nClave '{key}':")
        print(result[:200] + "..." if len(result) > 200 else result)
        
        # Buscar palabras indonesias comunes
        if any(word in result.upper() for word in ['DAN', 'UNTUK', 'YANG', 'INI', 'ADALAH']):
            print(f"*** POSIBLE SOLUCIÓN CON CLAVE '{key}' ***")

def try_caesar_with_key(ciphertext, key):
    """Intenta Caesar con clave específica"""
    result = ""
    for char in ciphertext:
        if 'A' <= char <= 'Z':
            result += chr((ord(char) - ord('A') + key) % 26 + ord('A'))
        elif 'a' <= char <= 'z':
            result += chr((ord(char) - ord('a') + key) % 26 + ord('a'))
        else:
            result += char
    return result

def try_caesar_analysis(ciphertext):
    """Analiza Caesar con diferentes claves"""
    print("\n=== ANÁLISIS CAESAR ===")
    
    for key in range(1, 26):
        result = try_caesar_with_key(ciphertext, key)
        if any(word in result.upper() for word in ['DAN', 'UNTUK', 'YANG', 'INI', 'ADALAH', 'DARI', 'PADA']):
            print(f"Clave {key}: {result[:200]}...")
            if 'DAN' in result.upper() or 'UNTUK' in result.upper():
                print(f"*** POSIBLE SOLUCIÓN CON CLAVE {key} ***")

if __name__ == "__main__":
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    analyze_indonesian_patterns(ciphertext)
    try_vigenere_analysis(ciphertext)
    try_caesar_analysis(ciphertext)