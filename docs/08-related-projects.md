# 08 — Bog'liq loyihalar va resurslar

Bu loyiha bir nechta boshqa loyiha/tajribalar bilan chambarchas bog'liq.
Barcha natijalar **yo'qolmagan** — quyida xarita.

## uz-llm-lab (asosiy hamkor loyiha)

**Manzil:** `../uz-llm-lab/` · **GitHub:** `ozodbekprog/uz-llm-lab` (private)

| Nima | Joy |
|---|---|
| KRONOS hujjatlari (Falcon3-10B, Vulkan) | `kronos/BOSQICH0_hisobot.md`, `BOSQICH234_natijalar.md` |
| **SPEED-50 natijalari (Maple 67 tok/s)** | `kronos/SPEED50_natijalar.md` |
| Agentlar uchun brifing | `HANDOFF.md` |
| I2_S→TQ2_0 transkoder | `kronos/i2s_to_tq2_0.py` |
| Kronecker probe | `kronos/kronecker_probe.py` |
| Maple/A falcon loglari | `logs/results_maple_speed50.json`, `results_maple_api.json` |
| Falcon3 model GGUF'lar | `models/gguf/Falcon3-10B-Instruct-1.58bit-tq2_0.gguf` |
| **llama.cpp Vulkan build** | `tools/llama-vulkan/bin/` (bu loyiha ishlatadi) |
| BitNet/Falcon bitnet.cpp | `bitnet/` |

**Git commitlar:** `6206e48` (SPEED-50+KRONOS), `829d97e` (10B optimizatsiya), `64d577c` (ternary tajribalar)

## llama-prism (foydalanuvchi kloni)

**Manzil:** `~/llama-prism/` — PrismML-Eng/llama.cpp (prism branch, commit bdc23b5)
- CUDA PTQ1_0 MMQ kernels (Ampere GPU'lar uchun — GTX 1650'da ishlamaydi)
- Bonsai ternary modellar bilan tajriba uchun

## Asosiy texnologiyalar (qayerdan olingan)

| Komponent | Manba |
|---|---|
| llama.cpp mainline 7ab4ee7 | Vulkan build (TQ2_0/MoE shaderlar) |
| Qwen2.5 modellar | HF (bartowski/Qwen/ggml-org) |
| alloma-8B | `kmamaroziqov/alloma-8b-q4` (community GGUF) |
| Maple-Preview 20B-A1B | `deepgrove/maple-preview-GGUF` (KRONOS loyihasi) |
| Semantic encoder | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |

## Xotira bazasi (Fariza)

Muhim faktlar SQLite'da: `~/.fariza/config/opencode/memory/memory.db`
```bash
python3 ~/.fariza/config/opencode/memory/memory.py search "Maple"   # 67 tok/s
python3 ~/.fariza/config/opencode/memory/memory.py search "TQ2_0"   # kichraytirish
python3 ~/.fariza/config/opencode/memory/memory.py search "SASORI"  # rad etilgan
```

## O'zaro bog'liqlik diagrammasi

```
uz-llm-lab                          slm-orchestrator (bu loyiha)
├── kronos/ (SPEED-50, KRONOS)      ├── src/ (router, orchestrator)
├── tools/llama-vulkan ◄────────────┤── (llama-server ishlatiladi)
├── bitnet/models/ (Falcon3...)     ├── models/ (5 mutaxassis + router)
└── logs/ (Results)                 └── docs, daily, experiments, results
        ▲                                    ▲
        └──── ~/llama-prism (PrismML) ───────┘
              (kelajakdagi ternary tajribalar)
```

## Muhim: natijalar takrorlanmasligi uchun

Bir xil tajribani qayta o'tkazishdan oldin tekshiring:
1. `experiments/` — gipoteza/natija/xulosa bormi?
2. `docs/06-failed-attempts.md` — avval sinab ko'rilganmi?
3. Xotira bazasi — fakt yozilganmi?
