#!/bin/bash
for i in {1..5}; do
  echo "=== Intento $i ==="
  timeout 40 python3 /workspace/simple_attack.py
  if [ -f /workspace/aes_enc.bin ]; then
    echo "¡Encontrado!"
    exit 0
  fi
done
echo "No encontrado en 5 intentos"
