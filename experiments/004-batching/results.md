# Tajriba 004: Batching — Natijalar

## O'lchangan (math, 64 token javob, --parallel 8)

| Parallel | Wall | Tokens | Aggregate | Per-stream |
|---:|---:|---:|---:|---:|
| 1 | 1.07s | 64 | 60.0 tok/s | 60.0 |
| **2** | 1.03s | 128 | **124.6 tok/s** | 62.3 |
| 4 | 2.46s | 205 | 83.3 tok/s | 21.9 |
| 8 | 6.86s | 512 | 74.7 tok/s | 9.3 |

## Tahlil
1. **n=2 da ideal scaling** (+108%) — og'irliklar 2 token uchun bir marta o'qildi
2. **n=4/8 da degradatsiya** — overhead/contention (attention, KV, HTTP, scheduling)
3. n=1 nima uchun 60 (bench 102 emas)? — HTTP + prompt processing + chat template
   qo'shimcha ~0.4s (fixed cost)

## Nazariy chegara
- Bitta oqim: 167GB/s ÷ 1.1GB = **151 tok/s** (100% BW da)
- Batching linear scaling bersa n=2 da ~300 tok/s bo'lardi — real 124.6

## Fayllar
- `scripts/batch_bench.py`
