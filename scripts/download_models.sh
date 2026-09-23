#!/bin/bash
# 5 mutaxassis modelni yuklab olish (aria2, 8 oqim)
# DIQQAT: allaqachon yuklangan bo'lsa o'tkazib yuboradi
cd "$(dirname "$0")/.." || exit 1
mkdir -p models/{math,code,chat,image,uz} logs/inference

dl() {
  local tag=$1 repo=$2 file=$3
  [ -s "models/$tag/$tag.gguf" ] && { echo "[$tag] bor"; return 0; }
  echo "[$tag] yuklanmoqda..."
  aria2c -x 8 -s 8 -k 1M --file-allocation=none --retry-wait 5 -m 5 \
    -d "models/$tag" -o "$tag.gguf" \
    "https://huggingface.co/$repo/resolve/main/$file" > "logs/inference/dl_$tag.log" 2>&1
  echo "[$tag] $(du -h "models/$tag/$tag.gguf" 2>/dev/null | cut -f1 || echo XATO)"
}

dl math  bartowski/Qwen2.5-Math-1.5B-Instruct-GGUF "Qwen2.5-Math-1.5B-Instruct-Q4_K_M.gguf"
dl code  Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF     "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
dl chat  Qwen/Qwen2.5-1.5B-Instruct-GGUF           "qwen2.5-1.5b-instruct-q4_k_m.gguf"
dl image ggml-org/Qwen2-VL-2B-Instruct-GGUF        "Qwen2-VL-2B-Instruct-Q4_K_M.gguf"
[ -s models/image/mmproj.gguf ] || aria2c -x 8 -s 8 -k 1M --file-allocation=none \
  -d models/image -o mmproj.gguf \
  "https://huggingface.co/ggml-org/Qwen2-VL-2B-Instruct-GGUF/resolve/main/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf"
dl uz    kmamaroziqov/alloma-8b-q4                 "Model-8.0B-Q4_K_M.gguf"

echo "Tayyor!"
