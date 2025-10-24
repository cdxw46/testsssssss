#!/usr/bin/env python3

def detailed_flag_analysis():
    """Análisis detallado de la flag"""
    print("=== ANÁLISIS DETALLADO DE LA FLAG ===")
    
    flag_cipher = "34F{6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    expected = "FGTE{HURUF_BESAR_SEMUA}"
    
    print(f"Flag cifrada: {flag_cipher}")
    print(f"Flag esperada: {expected}")
    print()
    
    # Extraer solo el contenido interno
    cipher_inner = flag_cipher[4:-1]  # Sin 34F{ y }
    expected_inner = expected[4:-1]   # Sin FGTE{ y }
    
    print(f"Contenido cifrado: {cipher_inner}")
    print(f"Contenido esperado: {expected_inner}")
    print(f"Longitud cifrado: {len(cipher_inner)}")
    print(f"Longitud esperado: {len(expected_inner)}")
    print()
    
    # Analizar carácter por carácter
    print("=== ANÁLISIS CARÁCTER POR CARÁCTER ===")
    print("Cifrado: ", end="")
    for i, char in enumerate(cipher_inner):
        print(f"{char:2}", end="")
    print()
    
    print("Esperado:", end="")
    for i, char in enumerate(expected_inner):
        print(f"{char:2}", end="")
    print()
    
    print("Índices: ", end="")
    for i in range(len(expected_inner)):
        print(f"{i:2}", end="")
    print()
    
    # Intentar mapear los primeros caracteres
    print("\n=== MAPEO INICIAL ===")
    for i in range(min(len(cipher_inner), len(expected_inner))):
        print(f"{cipher_inner[i]} -> {expected_inner[i]}")
    
    # Buscar patrones en el cifrado
    print("\n=== ANÁLISIS DE PATRONES ===")
    
    # Buscar repeticiones
    print("Caracteres únicos en el cifrado:")
    unique_chars = set(cipher_inner)
    print(sorted(unique_chars))
    
    print("\nFrecuencia de caracteres:")
    freq = {}
    for char in cipher_inner:
        freq[char] = freq.get(char, 0) + 1
    
    for char, count in sorted(freq.items(), key=lambda x: x[1], reverse=True):
        print(f"'{char}': {count}")
    
    # Buscar si hay un patrón de sustitución simple
    print("\n=== BÚSQUEDA DE PATRONES DE SUSTITUCIÓN ===")
    
    # Intentar mapeo directo de los primeros caracteres
    mapping = {}
    for i in range(min(len(cipher_inner), len(expected_inner))):
        if cipher_inner[i] not in mapping:
            mapping[cipher_inner[i]] = expected_inner[i]
    
    print(f"Mapeo inicial: {mapping}")
    
    # Aplicar el mapeo al texto completo
    full_cipher = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    result = ""
    for char in full_cipher:
        if char in mapping:
            result += mapping[char]
        else:
            result += char
    
    print(f"\nResultado con mapeo inicial:")
    print(result[:300] + "..." if len(result) > 300 else result)

def try_alternative_flag_mapping():
    """Intenta mapeos alternativos para la flag"""
    print("\n=== MAPEOS ALTERNATIVOS ===")
    
    # Tal vez el cifrado no es directo, sino que hay caracteres de relleno
    flag_cipher = "6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM("
    expected = "HURUF_BESAR_SEMUA"
    
    # Intentar ignorar ciertos caracteres
    print("Intentando ignorar paréntesis y números:")
    
    # Extraer solo letras del cifrado
    cipher_letters = ''.join([c for c in flag_cipher if c.isalpha()])
    print(f"Letras del cifrado: {cipher_letters}")
    print(f"Letras esperadas: {expected}")
    print(f"Longitudes: {len(cipher_letters)} vs {len(expected)}")
    
    if len(cipher_letters) == len(expected):
        print("\nMapeo letra por letra:")
        for i, (cipher_char, expected_char) in enumerate(zip(cipher_letters, expected)):
            print(f"{cipher_char} -> {expected_char}")
    
    # Intentar mapeo con números
    print("\nIntentando mapeo con números:")
    cipher_alphanum = ''.join([c for c in flag_cipher if c.isalnum()])
    print(f"Alfanuméricos del cifrado: {cipher_alphanum}")
    print(f"Esperado: {expected}")
    print(f"Longitudes: {len(cipher_alphanum)} vs {len(expected)}")
    
    if len(cipher_alphanum) == len(expected):
        print("\nMapeo alfanumérico:")
        for i, (cipher_char, expected_char) in enumerate(zip(cipher_alphanum, expected)):
            print(f"{cipher_char} -> {expected_char}")

if __name__ == "__main__":
    detailed_flag_analysis()
    try_alternative_flag_mapping()