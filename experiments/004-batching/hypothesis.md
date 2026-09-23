# Tajriba 004: Batching — Gipoteza

## Gipoteza
Bir vaqtda bir nechta so'rovga xizmat qilish (continuous batching)
aggregate tok/s ni oshiradi — chunki og'irliklar har batch uchun
bir marta o'qiladi.

## Usul
```bash
llama-server -m math.gguf --parallel 8 -c 16384
# keyin: concurrent httpx requests (n=1,2,4,8)
.venv/bin/python scripts/batch_bench.py --port 8101
```

## Kutilayotgan Natija
| Parallel | Aggregate | Per-stream |
|---:|---|---|
| 1 | ~60 | 60 |
| 2 | ~120 | 60 |
| 4 | ~240 | 60 |
| 8 | ~480 | 60 |

(ideal lineer scaling)
