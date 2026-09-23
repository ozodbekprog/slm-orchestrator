#!/bin/bash
# Router LoRA o'qitish
cd "$(dirname "$0")/.." || exit 1

echo "=== Router o'qitish (Qwen2.5-0.5B + LoRA) ==="
echo "Dataset: $(wc -l < data/router_train.jsonl) train / $(wc -l < data/router_eval.jsonl) eval"
echo "Vaqt: ~22 daqiqa (GTX 1650, fp32)"
echo ""

.venv/bin/python src/router/train_router.py "$@" 2>&1 | tee logs/training/train_$(date +%Y%m%d_%H%M).log

echo ""
echo "Natija: models/router/lora_adapter/"
echo "Metrikalar: logs/training/router_results.json"
