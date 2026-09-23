#!/bin/bash
# Umumiy benchmark skripti
cd "$(dirname "$0")/.." || exit 1
B=../uz-llm-lab/tools/llama-vulkan/bin/llama-bench

echo "=== SLM Orkestrator Benchmark $(date) ==="
echo ""
echo "## Router"
.venv/bin/python src/router/predict.py "Solve 3x+5=20" 2>/dev/null | tail -3

echo ""
echo "## Mutaxassislar (tg16, -ngl 99)"
for m in math code chat image; do
  printf "%-7s " "$m"
  $B -m "models/$m/$m.gguf" -p 64 -n 16 -t 8 -ngl 99 -dev Vulkan1 2>/dev/null \
    | grep "tg16" | awk -F'|' '{gsub(/ /,"",$(NF-1)); print $(NF-1)}'
done
printf "%-7s " "uz"
$B -m models/uz/uz.gguf -p 64 -n 16 -t 8 -ngl 20 -dev Vulkan1 2>/dev/null \
  | grep "tg16" | awk -F'|' '{gsub(/ /,"",$(NF-1)); print $(NF-1)}'

echo ""
echo "## E2E (orchestrator ishlab turganida)"
if curl -sf --max-time 2 http://127.0.0.1:8200/health >/dev/null 2>&1; then
    .venv/bin/python scripts/e2e_test.py 2>/dev/null | tail -8
else
    echo "  orchestrator o'chiq (:8200)"
fi
