#!/bin/bash
# Kunlik hisobot yaratish
cd "$(dirname "$0")/.." || exit 1

DATE=$(date +%Y-%m-%d)
FILE="daily/$DATE.md"

if [ ! -f "$FILE" ]; then
    cp daily/TEMPLATE.md "$FILE"
    echo "Yaratildi: $FILE"
fi

{
  echo ""
  echo "---"
  echo "## Avtomatik holat ($(date +%H:%M))"
  echo ""
  echo "- CPU: $(lscpu | grep 'Model name' | cut -d: -f2 | xargs)"
  echo "- RAM: $(free -h | grep Mem | awk '{print $3"/"$2}')"
  echo "- GPU: $(nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader)"
  echo "- Orchestrator: $(curl -s --max-time 2 http://127.0.0.1:8200/health || echo 'o`chiq')"
  echo ""
  echo "### Modellar"
  find models -maxdepth 2 -name "*.gguf" -exec ls -lh {} \; 2>/dev/null | awk '{print "- "$9": "$5}'
} >> "$FILE"

echo "Hisobot yangilandi: $FILE"
