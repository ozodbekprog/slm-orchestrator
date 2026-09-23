# Natijalar — Umumiy Xulosa

**Sana:** 2026-09-23 · **Tizim:** HP Victus (i5-12450H, 15GB, GTX 1650 4GB)

## Asosiy raqamlar

| Komponent | Natija | Holat |
|---|---|---|
| Router (gibrid) | 98.9% aniqlik, 17.6 ms | ✅ |
| Router (real 20 savol) | 19/20 = 95% | ✅ |
| Mutaxassislar (4 ta) | 101-103 tok/s | ✅ |
| uz (alloma-8B) | 12.4 tok/s | ⚠️ |
| E2E (64 token) | median 742 ms | ✅ |
| E2E (qisqa) | ~300 ms | ✅ |
| Batching peak (n=2) | 124.6 tok/s | ✅ |
| Hajm | ~11 GB (5 model) | ✅ |

## Taqqoslash

| Yondashuv | Hajm | Tezlik | Sifat |
|---|---|---|---|
| 70B model (lokal) | 43GB+ | ishlamaydi | — |
| Bitta 8B model | 4.6GB | 12-20 tok/s | o'rta |
| **SLM Orkestrator** | 11GB | **102 tok/s** | mutaxassis sifati |

## Fayllar
- Router: [router/accuracy.md](router/accuracy.md), [router/latency.md](router/latency.md)
- Mutaxassislar: [experts/](experts/)
- E2E: [e2e/benchmark.md](e2e/benchmark.md)
