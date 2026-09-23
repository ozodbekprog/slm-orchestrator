# Loyiha Holati

**Oxirgi yangilanish:** 2026-09-23

## Komponentlar

| Komponent | Holat | Izoh |
|---|---|---|
| Router (Semantic) | ✅ | 92.1%, 18-29 ms CPU, multilingual MiniLM |
| Router (LoRA) | ✅ | 99.95%, ~100 ms CPU (Qwen0.5B + LoRA r16) |
| Router (Gibrid) | ✅ | 98.9%, threshold 0.5 |
| math mutaxassis | ✅ | Qwen2.5-Math-1.5B Q4_K_M, 102 tok/s |
| code mutaxassis | ✅ | Qwen2.5-Coder-1.5B Q4_K_M, 102.6 tok/s |
| chat mutaxassis | ✅ | Qwen2.5-1.5B Q4_K_M, 102.6 tok/s |
| image mutaxassis | ✅ | Qwen2-VL-2B + mmproj, 101 tok/s (tushunish) |
| uz mutaxassis | ⚠️ | alloma-8B Q4, 12.4 tok/s (ngl 20 qismli), sifat glitchlari |
| Orchestrator | ✅ | FastAPI :8200, chat UI, LRU=1, warmup |
| Meta-Learner | ⏳ | Rejalashtirilgan |

## Performance (o'lchangan)

| Metrika | Hozir | Maqsad | Holat |
|---|---|---|---|
| Router aniqlik | 98.9% | 95% | ✅ |
| Router latency (fast) | 5-29 ms | 20 ms | ✅ |
| Router latency (fallback) | ~100 ms | — | OK |
| Mutaxassis tok/s | 101-103 | 90 | ✅ |
| E2E latency | 0.7-2.3 s | <1 s (qisqa) | ✅ |
| Wall throughput | 45.8 tok/s | 50 | ⚠️ |
| Batching aggregate | 124.6 tok/s (n=2) | 217 | ❌ (fizik chegara) |

## Ma'lum cheklovlar

1. **VRAM 4GB** — bir vaqtda 1 mutaxassis; almashish 5-20s
2. **uz sifati** — alloma-8B glitch + qismli offload
3. **217 tok/s maqsad** — bu apparatda erishilmaydi (nazariy 151 tok/s)
4. **TQ2_0 fayllar** — `models/_attic/` da (buzilgan, 4.9GB)

## Keyingi Qadamlar

1. Spec-decode test (1.5B + Qwen0.5B draft)
2. Batching n=2 ni orchestratorga ulash
3. uz uchun alloma-3B yoki boshqa variant sinash
4. systemd user service (reboot survivability)
5. Meta-Learner qo'shish
