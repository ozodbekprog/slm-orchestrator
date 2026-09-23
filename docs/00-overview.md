# 00 — Loyiha haqida

## Muammo
Katta modellar (70B+) lokal ishlatish uchun kuchli apparat kerak. HP Victus
(16GB RAM, 4GB VRAM) bunday modellarni ko'tara olmaydi.

## Yechim
Bitta katta model o'rniga — **bir nechta kichik mutaxassis** + ularni
savolga qarab yo'naltiruvchi **router**.

```
Katta model:  1 × 70B  → 43GB RAM, sekin
SLM Orkestrator: 5 × (1.5-8B) → 11GB, tez, arzon
```

## Nima uchun ishlaydi?
1. **Mutaxassis effekti**: math modeli matematikada katta general modeldan
   kam bo'lmagan (Qwen2.5-Math), lekin 40x kichik.
2. **Router arzon**: routing qarori 5-30ms (semantic) — model o'zi emas.
3. **Lokal**: internet/API kerak emas, 0$ xarajat.

## Asosiy raqamlar (o'lchangan)

| | Qiymat |
|---|---|
| Router aniqlik | 98.9% (gibrid) |
| Router latency | 5-29 ms |
| Mutaxassis tezlik | 101-103 tok/s |
| Hajm | ~11 GB (Q4_K_M) |
| E2E | 0.7-2.3 s |

## Cheklovlar
- 4GB VRAM → bir vaqtda 1 mutaxassis (almashish 5-20s)
- uz (8B) sekin: 12.4 tok/s
- Post-hoc ternary ishlamaydi (QAT kerak)

## Repo tuzilmasi
Batafsil: [01-architecture.md](01-architecture.md),
[02-components.md](02-components.md)
