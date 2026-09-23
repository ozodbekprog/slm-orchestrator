#!/bin/bash
# Muhitni tekshirish va sozlash
cd "$(dirname "$0")/.." || exit 1

echo "=== SLM Orkestrator setup ==="
echo ""
echo "Python: $(.venv/bin/python --version 2>/dev/null || echo 'venv yo`q')"
.venv/bin/python scripts/check_env.py 2>/dev/null || {
    echo "check_env.py topilmadi — asosiy tekshiruv:"
    .venv/bin/python -c "import torch, transformers, peft, fastapi; print('paketlar OK')"
}
echo ""
echo "llama.cpp (Vulkan):"
LLAMA=../uz-llm-lab/tools/llama-vulkan/bin/llama-server
[ -x "$LLAMA" ] && echo "  ✅ $LLAMA" || echo "  ❌ yo'q — qayta build kerak"
echo ""
echo "Modellar:"
for m in math code chat image uz; do
    f="models/$m/$m.gguf"
    [ -f "$f" ] && echo "  ✅ $f ($(du -h "$f" | cut -f1))" || echo "  ❌ $f"
done
[ -f models/image/mmproj.gguf ] && echo "  ✅ models/image/mmproj.gguf" || echo "  ❌ mmproj"
echo ""
echo "Router adapter:"
[ -f models/router/lora_adapter/adapter_model.safetensors ] \
    && echo "  ✅ models/router/lora_adapter" || echo "  ❌ adapter yo'q (o'qitish kerak)"
