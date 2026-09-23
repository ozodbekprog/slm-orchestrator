# 03 — Benchmark natijalari (o'lchangan, 2026-09-23)

## Router

| Konfiguratsiya | Aniqlik | Latency (median) | Izoh |
|---|---|---|---|
| Semantic (5 route) | 92.1% | 13.7 ms (GPU) / 18-29 ms (CPU) | O'qitishsiz |
| Sof LoRA | 99.95% | 35 ms (GPU) / ~100 ms (CPU) | Qwen0.5B + LoRA |
| **Gibrid (thr 0.5)** | **98.9%** | **17.6 ms** | 34% fallback |
| Gibrid (thr 0.55) | 99.65% | — | 45.5% fallback |
| Gibrid (thr 0.60) | 99.75% | — | 58.4% fallback |

Eval: 2000 namuna (data/router_eval.jsonl).
Real 20 savol testi: **19/20 = 95%** (xato: uz-kod edge case).

## Mutaxassislar (llama-bench, tg16, -ngl 99)

| Model | pp64 | tg16 | GPU |
|---|---:|---:|---|
| math (1.5B Q4_K_M) | 966 | **102.0** | Vulkan |
| code (1.5B Q4_K_M) | 1008 | **102.6** | Vulkan |
| chat (1.5B Q4_K_M) | 1007 | **102.6** | Vulkan |
| image (2B Q4_K_M) | 1006 | **101.0** | Vulkan |
| uz (8B Q4, ngl 20) | 129 | **12.4** | qismli offload |

## E2E (orchestrator orqali)

| Savol | Route | tok/s | E2E |
|---|---|---:|---:|
| "What is 2+2?" | math | 92.7 | 2.3 s |
| "Say hello in one sentence." | chat | 82.0 | 3.3 s |
| "Salom, qalaysiz?" | uz | 5.7 | 6.3 s |
| 20 savol benchmark | — | med 97.2 | med 742 ms* |

*E2E median 742 ms = ~64 token generatsiya (0.66s) + router + HTTP.
Qisqa javob (16-32 token) bilan ~300 ms.

## Batching (math, --parallel 8)

| Parallel | Aggregate | Per-stream |
|---:|---:|---:|
| 1 | 60.0 | 60.0 |
| **2** | **124.6** | 62.3 |
| 4 | 83.3 | 21.9 |
| 8 | 74.7 | 9.3 |

**Xulosa:** n=2 optimal. 217 tok/s maqsad erishilmaydi (nazariy chegara 151).

## Hajm

| To'plam | Hajm |
|---|---|
| 5 mutaxassis (Q4_K_M) | ~10 GB |
| Router (LoRA) | 35 MB |
| Dataset | ~2 MB |
| _attic (buzilgan TQ2_0) | 4.9 GB |

## Xotira

| Rejim | VRAM | RAM |
|---|---|---|
| math/code/chat/image xizmatda | ~1.2-1.7 GB | ~2-3 GB |
| uz xizmatda | ~3.2 GB | ~4 GB |
| Orchestrator (router CPU) | 0 | ~1.5 GB |
