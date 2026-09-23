#!/bin/bash
# SLM Orkestrator — QADAM 3: 5 mutaxassis GGUF Q4_K_M ni background'da yuklash.
# Har model: aria2 (8 oqim). Jami ~11 GB. Log: logs/dl_<tag>.log
cd "$(dirname "$0")/.." || exit 1
D=models/specialists
mkdir -p "$D" logs

dl() {
  local tag=$1 repo=$2 file=$3
  if [ -s "$D/$tag.gguf" ]; then
    echo "[$tag] allaqachon bor: $(du -h "$D/$tag.gguf" | cut -f1)"
    return 0
  fi
  echo "[$tag] yuklanmoqda: $repo/$file"
  aria2c -x 8 -s 8 -k 1M --file-allocation=none --retry-wait 5 -m 5 \
    -d "$D" -o "$tag.gguf" \
    "https://huggingface.co/$repo/resolve/main/$file" > "logs/dl_$tag.log" 2>&1
  if [ -s "$D/$tag.gguf" ]; then
    echo "[$tag] TAYYOR: $(du -h "$D/$tag.gguf" | cut -f1)"
  else
    echo "[$tag] XATO — logs/dl_$tag.log ni ko'ring"
  fi
}

dl math        bartowski/Qwen2.5-Math-1.5B-Instruct-GGUF "Qwen2.5-Math-1.5B-Instruct-Q4_K_M.gguf"
dl code        Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF     "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
dl chat        Qwen/Qwen2.5-1.5B-Instruct-GGUF           "qwen2.5-1.5b-instruct-q4_k_m.gguf"
dl image       ggml-org/Qwen2-VL-2B-Instruct-GGUF        "Qwen2-VL-2B-Instruct-Q4_K_M.gguf"
dl image_mmproj ggml-org/Qwen2-VL-2B-Instruct-GGUF       "mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf"
dl uz          kmamaroziqov/allama-8b-q4                 "Model-8.0B-Q4_K_M.gguf"

echo DONE > logs/specialists_done
echo "=== Barcha yuklab olishlar tugadi ==="
du -sh "$D"
