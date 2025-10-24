#!/usr/bin/env python3

import base64
import re

def htb_analysis():
    message = "=EDMxETMxEDMgATMxEDMwEDMgEDMxATMwEDMgATMxADMwEDMgETMxETMwEDMgEDMwETMwEDMgATMwATMwEDMgEDMwADMwEDMgATMxEDMwEDMgEDMwEDMwEDMgATMwADMwEDMgETMxETMwEDMgADMxADMwEDMgATMxEDMwEDMgEDMwADMwEDMgETMxETMwEDMgEDMxADMwEDMgETMwATMwEDMgATMwATMwEDMgADMwATMxADMgEDMxEDMwEDMgETMwETMxEDMgEDMxADMwEDMgADMxATMwEDMgETMxADMwEDMgATMxADMwEDM"
    
    # Remover el = del inicio
    if message.startswith('='):
        message = message[1:]
    
    print("Análisis del patrón HTB:")
    print("="*50)
    
    # Mapeo que produce HTB{
    mapping = {
        'E': 'H', 'D': 'T', 'M': 'B', 'x': '{',
        'A': 'F', 'T': 'L', 'g': 'A', 'w': 'G'
    }
    
    # Aplicar mapeo
    result = ''.join([mapping.get(c, c) for c in message])
    print(f"Resultado con mapeo HTB: {result}")
    
    # Buscar patrones de flag
    flag_patterns = re.findall(r'HTB\{[^}]*\}', result)
    print(f"Patrones de flag encontrados: {flag_patterns}")
    
    # Buscar patrones más largos que podrían ser flags
    long_patterns = re.findall(r'HTB\{[A-Za-z0-9_]{10,}\}', result)
    if long_patterns:
        print(f"Patrones largos de flag: {long_patterns}")
    
    # Buscar patrones que contengan caracteres alfanuméricos
    alphanum_patterns = re.findall(r'HTB\{[A-Za-z0-9_]+\}', result)
    if alphanum_patterns:
        print(f"Patrones alfanuméricos de flag: {alphanum_patterns}")
    
    # Analizar el patrón de 4 caracteres original
    pattern = re.findall(r'.{4}', message)
    print(f"\nPatrones de 4 caracteres: {len(pattern)}")
    
    # Buscar patrones que podrían formar una flag completa
    print(f"\nBuscando patrones que podrían formar una flag completa:")
    
    # Intentar diferentes longitudes de flag
    for length in range(10, 50):
        flag_pattern = f'HTB\\{{[A-Za-z0-9_]{{{length}}}\\}}'
        matches = re.findall(flag_pattern, result)
        if matches:
            print(f"Flags de longitud {length}: {matches}")
    
    # Buscar el patrón más largo que empiece con HTB{
    htb_start = result.find('HTB{')
    if htb_start != -1:
        print(f"\nPrimera ocurrencia de HTB{{ en posición: {htb_start}")
        
        # Buscar el cierre de la flag
        close_pos = result.find('}', htb_start)
        if close_pos != -1:
            potential_flag = result[htb_start:close_pos + 1]
            print(f"Posible flag: {potential_flag}")
        else:
            print("No se encontró el cierre de la flag")
    
    # Buscar todas las ocurrencias de HTB{
    htb_positions = [m.start() for m in re.finditer('HTB{', result)]
    print(f"\nPosiciones de HTB{{: {htb_positions}")
    
    # Analizar cada ocurrencia
    for i, pos in enumerate(htb_positions):
        print(f"\nOcurrencia {i+1} en posición {pos}:")
        
        # Buscar el cierre de la flag
        close_pos = result.find('}', pos)
        if close_pos != -1:
            potential_flag = result[pos:close_pos + 1]
            print(f"  Posible flag: {potential_flag}")
            
            # Verificar si parece una flag válida
            if len(potential_flag) > 5 and potential_flag[4:].replace('_', '').isalnum():
                print(f"  *** FLAG VÁLIDA ENCONTRADA: {potential_flag} ***")
        else:
            print("  No se encontró el cierre de la flag")
    
    # Intentar decodificar como base64 después del mapeo
    print(f"\n--- Intentando decodificar como base64 después del mapeo ---")
    
    try:
        # Agregar padding si es necesario
        if len(result) % 4 != 0:
            padding_needed = 4 - (len(result) % 4)
            result_padded = result + '=' * padding_needed
        else:
            result_padded = result
        
        decoded = base64.b64decode(result_padded)
        print(f"Decodificado como base64: {decoded}")
        print(f"Como texto: {decoded.decode('utf-8', errors='ignore')}")
        
        # Buscar patrones de flag en el resultado decodificado
        flag_patterns_decoded = re.findall(r'[A-Za-z0-9_]{5,}', decoded.decode('utf-8', errors='ignore'))
        if flag_patterns_decoded:
            print(f"*** Posibles flags en resultado decodificado: {flag_patterns_decoded} ***")
            
    except Exception as e:
        print(f"Error en decodificación base64: {e}")
    
    # Intentar un mapeo diferente basado en el patrón HTB
    print(f"\n--- Intentando mapeo alternativo ---")
    
    # Mapeo alternativo que podría producir una flag más clara
    alt_mapping = {
        'E': 'H', 'D': 'T', 'M': 'B', 'x': '{',
        'A': 'F', 'T': 'L', 'g': 'A', 'w': 'G'
    }
    
    # Aplicar mapeo alternativo
    alt_result = ''.join([alt_mapping.get(c, c) for c in message])
    print(f"Resultado con mapeo alternativo: {alt_result}")
    
    # Buscar patrones de flag en el resultado alternativo
    alt_flag_patterns = re.findall(r'HTB\{[^}]*\}', alt_result)
    if alt_flag_patterns:
        print(f"Patrones de flag en resultado alternativo: {alt_flag_patterns}")
    
    return result, alt_result

if __name__ == "__main__":
    htb_analysis()