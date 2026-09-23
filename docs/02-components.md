# 02 — Komponentlar

## Router

| Fayl | Vazifa |
|---|---|
| `src/router/semantic_router_eval.py` | Semantic router + utterances + baholash |
| `src/router/hybrid_router_eval.py` | Gibrid router baholash (thresholdlar) |
| `src/router/predict.py` | Production RouterPredictor klassi + CLI |
| `src/router/train_router.py` | LoRA o'qitish (Qwen2.5-0.5B) |
| `models/router/lora_adapter/` | O'qitilgan adapter (35MB) |

## Orchestrator

| Fayl | Vazifa |
|---|---|
| `src/orchestrator/app.py` | FastAPI: chat UI + /ask + /route + LRU menejer |

## Mutaxassislar (models/)

| Papka | Model | Hajm | Port | Tezlik |
|---|---|---|---|---|
| `math/math.gguf` | Qwen2.5-Math-1.5B-Instruct Q4_K_M | 941M | 8101 | 102 tok/s |
| `code/code.gguf` | Qwen2.5-Coder-1.5B-Instruct Q4_K_M | 1.1G | 8102 | 102.6 tok/s |
| `chat/chat.gguf` | Qwen2.5-1.5B-Instruct Q4_K_M | 1.1G | 8103 | 102.6 tok/s |
| `image/image.gguf` + `mmproj.gguf` | Qwen2-VL-2B-Instruct Q4_K_M | 941M+677M | 8104 | 101 tok/s |
| `uz/uz.gguf` | alloma-8B (community Q4) | 4.6G | 8105 | 12.4 tok/s |
| `_attic/*` | Buzilgan TQ2_0 fayllar | 4.9G | — | ❌ |

## Dataset

| Fayl | Hajm |
|---|---|
| `data/router_train.jsonl` | 8000 namuna |
| `data/router_eval.jsonl` | 2000 namuna |
| `data/label_map.json` | 5 sinf xaritasi |

Sinflar: math · code · uz · chat · image (har biri 2000)

## Skriptlar

| Skript | Vazifa |
|---|---|
| `scripts/setup.sh` | Muhit tekshiruvi |
| `scripts/download_models.sh` | 5 mutaxassisni yuklab olish |
| `scripts/train_router.sh` | LoRA o'qitish |
| `scripts/test_specialists.sh` | Har mutaxassisni alohida sinash |
| `scripts/e2e_test.py` | End-to-end benchmark |
| `scripts/batch_bench.py` | Batching o'lchovi |
| `scripts/daily_report.sh` | Kunlik hisobot |
| `scripts/benchmark.sh` | Umumiy benchmark |

## Infratuzilma

| Element | Manzil |
|---|---|
| llama.cpp Vulkan build | `../uz-llm-lab/tools/llama-vulkan/bin/` |
| Python venv | `.venv → ../uz-llm-lab/.venv` (Python 3.12) |
| Loglar | `logs/{training,inference,errors}/` |
