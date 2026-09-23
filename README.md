# SLM Orkestrator + Meta-Learner

Bir nechta kichik mutaxassis modellarni **router** orqali birlashtirib, katta
modellarga yaqin sifatni **lokal, tez va arzon** olish tizimi.

**Apparat:** HP Victus · i5-12450H · 15GB RAM · GTX 1650 4GB · Fedora 44

## Hozirgi Holat (2026-09-23)

| Komponent | Holat | Natija |
|---|---|---|
| Router (Semantic) | ✅ | 92.1% aniqlik, 18-29 ms (CPU) |
| Router (LoRA) | ✅ | 99.95% aniqlik, ~100 ms (CPU) |
| Router (Gibrid) | ✅ | 98.9% aniqlik, 17.6 ms |
| Orchestrator (FastAPI) | ✅ | :8200, chat UI + API |
| math mutaxassis | ✅ | 102 tok/s |
| code mutaxassis | ✅ | 102.6 tok/s |
| chat mutaxassis | ✅ | 102.6 tok/s |
| image mutaxassis | ✅ | 101 tok/s (rasm tushunish) |
| uz mutaxassis | ⚠️ | 12.4 tok/s (alloma-8B qismli offload) |
| Meta-Learner | ⏳ | Rejalashtirilgan |

## Tez Boshlash

```bash
cd slm-orchestrator
.venv/bin/uvicorn src.orchestrator.app:app --host 127.0.0.1 --port 8200
# Brauzer: http://127.0.0.1:8200  (chat UI)
# Swagger: http://127.0.0.1:8200/docs
```

```bash
# Router testi
.venv/bin/python src/router/predict.py "Solve 3x + 5 = 20"
.venv/bin/python src/router/predict.py --tests

# E2E benchmark (orchestrator ishlab turganida)
.venv/bin/python scripts/e2e_test.py
```

## Arxitektura

```
query ─> Gibrid Router ─┬─ score >= 0.5 → mutaxassis (tez yo'l)
                        └─ score <  0.5 → LoRA fallback
                              │
        ┌──────┬──────┬───────┼───────┬───────┐
        math   code   chat   image    uz
       (8101) (8102) (8103)  (8104)  (8105)
```

Batafsil: [docs/01-architecture.md](docs/01-architecture.md)

## Muhim cheklovlar (o'lchangan)

- **VRAM 4GB** → bir vaqtda faqat 1 mutaxassis yuklanadi (LRU=1 almashish ~5-20s)
- **fp16 matmul bu GPU'da 5x sekin** (315 vs 1484 GFLOPS) → o'qitish fp32
- **nvcc yo'q** → llama.cpp **Vulkan** backend ishlatiladi (CUDA emas)
- **Post-hoc ternary (TQ2_0) modelni buzadi** → faqat nativ/QAT ternary modellar

## Natijalar

| Metrika | Qiymat |
|---|---|
| Router aniqlik | 98.9% |
| Router latency (fast path) | 5-29 ms |
| Mutaxassis tezligi | 101-103 tok/s |
| E2E (qisqa javob) | 0.7-2.3 s |
| Batching peak (n=2) | 124.6 tok/s aggregate |
| Hajm (5 mutaxassis) | ~11 GB (Q4_K_M) |

Batafsil: [docs/03-benchmarks.md](docs/03-benchmarks.md)

## Struktura

```
slm-orchestrator/
├── docs/          # Hujjatlar (00-07)
├── daily/         # Kunlik hisobotlar
├── agents/        # Agent hisobotlari (7 ta)
├── experiments/   # Tajribalar (001-004)
├── results/       # Natijalar (router/experts/e2e)
├── src/           # Kod (router, orchestrator, api...)
├── models/        # Modellar (math, code, chat, image, uz, router, _attic)
├── configs/       # Konfiguratsiyalar
├── logs/          # Loglar (training, inference, errors)
├── scripts/       # Skriptlar
└── tests/         # Testlar
```

## Litsenziya

Akademik tadqiqot uchun.
