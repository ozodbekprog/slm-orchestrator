# E2E Benchmark

## 20 savol (orchestrator :8200, max 64 token)

| Savol | Route | Router | E2E | tok/s | OK |
|---|---|---:|---:|---:|:--:|
| Solve 3x+5=20 | math | 6.6ms | 2349ms | 98 | ✅ |
| integral of sin(x) | math | 5.3ms | 738ms | 98 | ✅ |
| 5! nechaga teng? | uz | 6.0ms | — | — | ✅* |
| 15% of 240 | math | 5.8ms | 2241ms | 97 | ✅ |
| Flask 500 error | code | 6.9ms | 2353ms | 97 | ✅ |
| merge sorted lists | code | 5.6ms | 741ms | 97 | ✅ |
| SQL top customers | code | 5.6ms | 742ms | 97 | ✅ |
| TCP vs UDP | code | 40.3ms | 774ms | 97 | ✅ |
| kodda xato bormi | code | 5.9ms | 364ms | 97 | ❌ |
| Poytaxti qayerda | uz | 5.6ms | — | — | ✅* |
| kitob tavsiya | uz | 5.2ms | — | — | ✅* |
| Salom qalaysiz | uz | 5.7ms | — | — | ✅* |
| kayfiyatim yaxshi | uz | 5.6ms | — | — | ✅* |
| tired today | chat | 7.7ms | 2236ms | 97 | ✅ |
| Hello how are you | chat | 5.6ms | 332ms | 97 | ✅ |
| weather Tashkent | chat | 6.3ms | 740ms | 97 | ✅ |
| Draw futuristic car | image | 5.5ms | — | — | ✅* |
| Remove background | image | 22.1ms | — | — | ✅* |
| logo bakery | image | 22.8ms | — | — | ✅* |
| sketch 3D render | image | 22.5ms | — | — | ✅* |

\* — model hali yuklanmagan edi (uz/image keyin qo'shildi)

## Yig'ma metrikalar
| Metrika | Qiymat |
|---|---|
| Routing aniqlik | 19/20 = 95% |
| Router med latency | 5.8 ms |
| E2E med (xizmat ko'rsatilgan) | 742 ms |
| Mutaxassis med tezlik | 97.2 tok/s |
| Wall throughput | 45.8 tok/s |

## Keyin qo'shilgan testlar
| Test | Natija |
|---|---|
| math "7*6" | ✅ 92.6 tok/s |
| chat "Say hello..." | ✅ 82 tok/s (fix'dan keyin) |
| image (sintetik rasm) | ✅ OCR + tavsif, 98 tok/s |

JSON: `logs/inference/e2e_results.json`
