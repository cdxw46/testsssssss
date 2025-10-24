#!/usr/bin/env python3

def analyze_cipher(ciphertext):
    print("=== ANÁLISIS DEL CIFRADO ===")
    print(f"Longitud del texto: {len(ciphertext)}")
    print(f"Texto: {ciphertext}")
    print()
    
    # Análisis de frecuencia de caracteres
    freq = {}
    for char in ciphertext:
        if char.isalnum() or char in '(){}':
            freq[char] = freq.get(char, 0) + 1
    
    print("=== FRECUENCIA DE CARACTERES ===")
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    for char, count in sorted_freq:
        print(f"'{char}': {count}")
    
    print()
    
    # Análisis de patrones con paréntesis
    print("=== PATRONES CON PARÉNTESIS ===")
    import re
    paren_patterns = re.findall(r'\([^)]+\)', ciphertext)
    for pattern in paren_patterns:
        print(f"Patrón: {pattern}")
    
    print()
    
    # Análisis de números
    print("=== ANÁLISIS DE NÚMEROS ===")
    numbers = re.findall(r'\d+', ciphertext)
    print(f"Números encontrados: {numbers}")
    
    # Análisis de la flag
    print("=== ANÁLISIS DE LA FLAG ===")
    flag_match = re.search(r'34F\{[^}]+\}', ciphertext)
    if flag_match:
        flag_part = flag_match.group()
        print(f"Parte de la flag: {flag_part}")
        print(f"Caracteres únicos en la flag: {set(flag_part)}")

if __name__ == "__main__":
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    analyze_cipher(ciphertext)