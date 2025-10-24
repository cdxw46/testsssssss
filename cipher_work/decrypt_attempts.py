#!/usr/bin/env python3

def try_number_substitution(ciphertext):
    """Intenta sustituir números por letras"""
    print("=== INTENTO DE SUSTITUCIÓN NUMÉRICA ===")
    
    # Mapeo común de números a letras (A=1, B=2, etc.)
    num_to_letter = {
        '0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', 
        '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J'
    }
    
    result = ""
    for char in ciphertext:
        if char in num_to_letter:
            result += num_to_letter[char]
        else:
            result += char
    
    print("Resultado con A=0, B=1, etc.:")
    print(result[:200] + "..." if len(result) > 200 else result)
    print()
    
    # Mapeo alternativo (0=J, 1=A, 2=B, etc.)
    num_to_letter2 = {
        '0': 'J', '1': 'A', '2': 'B', '3': 'C', '4': 'D', 
        '5': 'E', '6': 'F', '7': 'G', '8': 'H', '9': 'I'
    }
    
    result2 = ""
    for char in ciphertext:
        if char in num_to_letter2:
            result2 += num_to_letter2[char]
        else:
            result2 += char
    
    print("Resultado con J=0, A=1, etc.:")
    print(result2[:200] + "..." if len(result2) > 200 else result2)
    print()

def try_rot13_variant(ciphertext):
    """Intenta ROT13 o variantes"""
    print("=== INTENTO ROT13 ===")
    
    def rot13_char(char):
        if 'A' <= char <= 'Z':
            return chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
        elif 'a' <= char <= 'z':
            return chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
        else:
            return char
    
    result = ""
    for char in ciphertext:
        result += rot13_char(char)
    
    print("Resultado ROT13:")
    print(result[:200] + "..." if len(result) > 200 else result)
    print()

def try_atbash(ciphertext):
    """Intenta cifrado Atbash"""
    print("=== INTENTO ATBASH ===")
    
    def atbash_char(char):
        if 'A' <= char <= 'Z':
            return chr(ord('Z') - (ord(char) - ord('A')))
        elif 'a' <= char <= 'z':
            return chr(ord('z') - (ord(char) - ord('a')))
        else:
            return char
    
    result = ""
    for char in ciphertext:
        result += atbash_char(char)
    
    print("Resultado Atbash:")
    print(result[:200] + "..." if len(result) > 200 else result)
    print()

def analyze_flag_section(ciphertext):
    """Analiza específicamente la sección de la flag"""
    print("=== ANÁLISIS DE LA FLAG ===")
    
    flag_start = ciphertext.find("34F{")
    if flag_start != -1:
        flag_end = ciphertext.find("}", flag_start)
        if flag_end != -1:
            flag_content = ciphertext[flag_start:flag_end+1]
            print(f"Flag cifrada: {flag_content}")
            
            # Intentar diferentes sustituciones en la flag
            flag_inner = flag_content[4:-1]  # Sin 34F{ y }
            print(f"Contenido interno: {flag_inner}")
            
            # Mapeo de números a letras para la flag
            num_to_letter = {
                '0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', 
                '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J'
            }
            
            flag_decoded = ""
            for char in flag_inner:
                if char in num_to_letter:
                    flag_decoded += num_to_letter[char]
                else:
                    flag_decoded += char
            
            print(f"Flag con A=0: {flag_decoded}")
            
            # Mapeo alternativo
            num_to_letter2 = {
                '0': 'J', '1': 'A', '2': 'B', '3': 'C', '4': 'D', 
                '5': 'E', '6': 'F', '7': 'G', '8': 'H', '9': 'I'
            }
            
            flag_decoded2 = ""
            for char in flag_inner:
                if char in num_to_letter2:
                    flag_decoded2 += num_to_letter2[char]
                else:
                    flag_decoded2 += char
            
            print(f"Flag con J=0: {flag_decoded2}")

if __name__ == "__main__":
    ciphertext = "F10K FMHQKD0KK06Q 0K JHMF 63 H U6Q4-F(MD (W(MP0K( F6 HKK(KK 30(UY H4(QF P6DDVQ0PHF06QK VQY(M HY5(MK( P6QY0F06QK. U640KF0PK F(HDK HM( F6 5(M03R HUU P1HQQ(UK JM06M F6 Y(JU6RD(QF HQY M(J6MF HQR P6DJM6D0K(K 0DD(Y0HF(UR. M(D(DN(M F1HF P6DJHMFD(QFHU0THF06Q 0K PM0F0PHU; 6QUR F16K( L0F1 Q((Y-F6-2Q6L K16VUY 1H5( HPP(KK F6 F1(K( Y(FH0UK. 03 F10K D(KKH4( 0K M(P65(M(Y HQY Y(PMRJF(Y, JM6P((Y F6 F1( Y(K04QHF(Y KH3(16VK( HQY HLH0F 3VMF1(M 0QKFMVPF06QK. 34F({6J(MHF06Q_Q041F3HUU_30QHU_M(J6MF_K(PVM(}"
    
    try_number_substitution(ciphertext)
    try_rot13_variant(ciphertext)
    try_atbash(ciphertext)
    analyze_flag_section(ciphertext)