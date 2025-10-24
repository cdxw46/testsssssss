#!/usr/bin/env python3

def analyze_cipher_detailed(ciphertext):
    print("=== ANÁLISIS DETALLADO DEL CIFRADO ===")
    print(f"Longitud del texto: {len(ciphertext)}")
    print()
    
    # Análisis de frecuencia de caracteres
    freq = {}
    for char in ciphertext:
        freq[char] = freq.get(char, 0) + 1
    
    print("=== FRECUENCIA DE CARACTERES ===")
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    for char, count in sorted_freq:
        print(f"'{char}': {count}")
    
    print()
    
    # Análisis de patrones con paréntesis - método manual
    print("=== PATRONES CON PARÉNTESIS ===")
    paren_count = 0
    in_paren = False
    current_paren = ""
    paren_patterns = []
    
    for i, char in enumerate(ciphertext):
        if char == '(':
            paren_count += 1
            in_paren = True
            current_paren = ""
        elif char == ')' and in_paren:
            paren_count += 1
            in_paren = False
            paren_patterns.append(f"({current_paren})")
            current_paren = ""
        elif in_paren:
            current_paren += char
    
    print(f"Total paréntesis: {paren_count}")
    for pattern in paren_patterns:
        print(f"Patrón: {pattern}")
    
    print()
    
    # Análisis de la flag específica
    print("=== ANÁLISIS DE LA FLAG ===")
    flag_start = ciphertext.find("34F{")
    if flag_start != -1:
        flag_end = ciphertext.find("}", flag_start)
        if flag_end != -1:
            flag_content = ciphertext[flag_start:flag_end+1]
            print(f"Flag completa: {flag_content}")
            print(f"Contenido de la flag: {flag_content[4:-1]}")
    
    print()
    
    # Análisis de patrones de sustitución
    print("=== ANÁLISIS DE SUSTITUCIÓN ===")
    # Buscar patrones comunes en cifrados clásicos
    print("Caracteres más frecuentes (posibles vocales):")
    for char, count in sorted_freq[:10]:
        print(f"'{char}': {count}")
    
    # Análisis de bigramas
    print("\n=== ANÁLISIS DE BIGRAMAS ===")
    bigrams = {}
    for i in range(len(ciphertext) - 1):
        bigram = ciphertext[i:i+2]
        if bigram.isalnum():
            bigrams[bigram] = bigrams.get(bigram, 0) + 1
    
    sorted_bigrams = sorted(bigrams.items(), key=lambda x: x[1], reverse=True)
    for bigram, count in sorted_bigrams[:15]:
        print(f"'{bigram}': {count}")

if __name__ == "__main__":
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    analyze_cipher_detailed(ciphertext)