#!/bin/bash
# Fayllarni tartibga solish (tarixni saqlagan holda)
# DIQQAT: mavjud tizim yo'llarini o'zgartiradi — app.py yangilangan bo'lishi kerak
cd "$(dirname "$0")/.." || exit 1

echo "=== SLM Orkestrator fayllarini tartibga solish ==="

mkdir -p docs daily agents experiments results src configs tests
mkdir -p models/{router,math,code,chat,image,uz,_attic}
mkdir -p logs/{training,inference,errors}

# Modellar (agar eski joyda bo'lsa)
mv models/specialists/math.gguf models/math/ 2>/dev/null
mv models/specialists/code.gguf models/code/ 2>/dev/null
mv models/specialists/chat.gguf models/chat/ 2>/dev/null
mv models/specialists/image.gguf models/image/ 2>/dev/null
mv models/specialists/image_mmproj.gguf models/image/mmproj.gguf 2>/dev/null
mv models/specialists/uz.gguf models/uz/ 2>/dev/null
mv models/specialists/*tq2_0*.gguf models/_attic/ 2>/dev/null

# Kod (agar eski joyda bo'lsa)
mv router/*.py src/router/ 2>/dev/null
mv router/lora_adapter models/router/lora_adapter 2>/dev/null
mv orchestrator/app.py src/orchestrator/app.py 2>/dev/null

# Loglar
mv logs/train_full.log logs/training/ 2>/dev/null
mv logs/router_results.json logs/training/ 2>/dev/null
mv logs/*router_results.json logs/inference/ 2>/dev/null
mv logs/e2e_results.json logs/inference/ 2>/dev/null

echo "Tartibga solindi! (hech narsa o'chirilmadi)"
echo ""
echo "Struktura:"
find . -maxdepth 2 -type d | grep -vE "\.venv|__pycache__|\.git" | sort
