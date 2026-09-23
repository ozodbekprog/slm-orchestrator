# 07 — Ishlaydigan Yechimlar Katalogi

## Router

| Yechim | Aniqlik | Latency | Holat |
|---|---|---|---|
| Semantic (MiniLM, CPU) | 92.1% | 18-29 ms | ✅ |
| LoRA (Qwen0.5B, CPU) | 99.95% | ~100 ms | ✅ |
| **Gibrid (thr 0.5)** | **98.9%** | **17.6 ms** | ✅ |

Kalit yechimlar:
- `encoder_device="cpu"` + `lora_device="cpu"` — VRAM tejash
- 12 ta salomlashish utterance — chat↔uz chalkashligini tuzatdi
- Startup warmup — birinchi LoRA chaqiruvni 418ms→100ms

## Mutaxassislar

| Model | Format | Tezlik | Holat |
|---|---|---|---|
| Qwen2.5-Math-1.5B | Q4_K_M | 102 tok/s | ✅ |
| Qwen2.5-Coder-1.5B | Q4_K_M | 102.6 tok/s | ✅ |
| Qwen2.5-1.5B | Q4_K_M | 102.6 tok/s | ✅ |
| Qwen2-VL-2B + mmproj | Q4_K_M | 101 tok/s | ✅ (tushunish) |
| alloma-8B | Q4 (community) | 12.4 tok/s | ⚠️ qismli |

## Optimizatsiyalar (tasdiqlangan)

| Texnologiya | Natija | Holat |
|---|---|---|
| `-ngl 99` (dense, <=2B) | to'liq GPU, 101-103 tok/s | ✅ |
| `--n-cpu-moe` (Maple MoE) | 67 tok/s (boshqa loyiha) | ✅ |
| `-ngl 20` + `-ot emb/head=CPU` (alloma) | 12.4 tok/s (CPU-only'dan tez) | ✅ |
| KV cache q8_0 | 2x tejash | ✅ |
| `--parallel 2` | 124.6 tok/s aggregate | ✅ |
| Startup warmup | 418→6 ms (fallback ~100ms) | ✅ |
| Batching n=2 | Peak aggregate | ✅ |
| LRU=1 lazy loading | 4GB VRAM bilan 5 mutaxassis | ✅ |

## llama.cpp build (Vulkan)

```bash
# build: /tmp/opencode/llama.cpp-main (reboot'da o'chadi — qayta klonlash kerak)
# doimiy: ../uz-llm-lab/tools/llama-vulkan/bin/ (patched RUNPATH=$ORIGIN)
llama-server -m <model.gguf> --port 810X -ngl 99 -c 4096 -t 8 -fa auto --parallel 1
```

## Python stack

| Paket | Versiya | Izoh |
|---|---|---|
| torch | 2.14.0+cu130 | CUDA ishlaydi |
| transformers | 5.17.0 | Qwen2/VL |
| peft | 0.21.0 | LoRA SEQ_CLS |
| sentence-transformers | 6.1.0 | multilingual MiniLM |
| fastapi/uvicorn | 0.141/0.53 | orchestrator |
| semantic-router | 0.1.16 | (ishlatildi, keyin custom) |

## Skriptlar

| Buyruq | Vazifa |
|---|---|
| `.venv/bin/uvicorn src.orchestrator.app:app --port 8200` | Server |
| `.venv/bin/python src/router/predict.py --tests` | Router testi |
| `.venv/bin/python scripts/e2e_test.py` | E2E benchmark |
| `bash scripts/test_specialists.sh` | Mutaxassis testlari |
| `.venv/bin/python scripts/batch_bench.py --port 8101` | Batching |
| `.venv/bin/python src/router/train_router.py` | LoRA qayta o'qitish |
