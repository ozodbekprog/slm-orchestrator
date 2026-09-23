# Agent-6: Benchmark — Natijalar

## Vazifa
Barcha komponentlarni o'lchash va jadvallarga keltirish.

## Asosiy natijalar

### Router
| Metrika | Qiymat |
|---|---|
| Gibrid aniqlik | 98.9% (2000 eval) |
| Real savollar | 19/20 = 95% |
| Fast path latency | 5-29 ms |
| Fallback latency | ~100 ms |

### Mutaxassislar (tg16)
| Model | tok/s |
|---|---:|
| math | 102.0 |
| code | 102.6 |
| chat | 102.6 |
| image | 101.0 |
| uz | 12.4 |

### E2E
| Metrika | Qiymat |
|---|---|
| Median (64 token) | 742 ms |
| Qisqa javob (16-32) | ~300 ms |
| Wall throughput | 45.8 tok/s |

### Batching
| Parallel | Aggregate |
|---:|---:|
| 2 | **124.6** |
| 4 | 83.3 |
| 8 | 74.7 |

## Metodologiya
- `llama-bench` (tg16, pp64, -ngl 99, Vulkan1)
- `scripts/e2e_test.py` (20 savol, API orqali)
- `scripts/batch_bench.py` (concurrent requests)

## Fayllar
- `docs/03-benchmarks.md`
- `logs/inference/*.json`
- `results/*`

## Eslatma
217 tok/s maqsad erishilmaydi: nazariy chegara 151 tok/s (167GB/s ÷ 1.1GB).
