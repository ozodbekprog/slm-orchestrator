# Agent-3: SASORI tekshiruvi — Natijalar

## Vazifa
SASORI ternary formatini tekshirish (5 modelni TQ3P ga o'tkazish).

## Natija: ❌ YAROQSIZ

| Da'vo | Tekshiruv | Natija |
|---|---|---|
| Konvertor mavjud | HF'da faqat 2 tayyor GGUF + binary runtime | ❌ Yo'q |
| 11GB → 1.4GB | TQ3P = 6.19 bpw → 14.5B×6.19/8 ≈ 11GB | ❌ Noto'g'ri |
| 217 tok/s | Muallif: 14B da 1.7-5.8 tok/s | ❌ |
| Zero-skip | Kernel value-independent (yo'q) | ❌ |

## Kontekst
- Repo: `FardoX/sasori-qwen3-14b-tq3p` (HF)
- Custom ggml type 43, patch yopiq, llama.cpp @6f3a9f3 kerak
- Faqat x86_64-avx2 runtime tar.gz (15MB binaries)

## Xulosa
SASORI — quality-per-bit format (K=3), tezlik uchun emas. Bizning maqsadga yaroqsiz.

## Fayllar
- `experiments/001-sasori/*`
- `models/_attic/` (TQ2_0 alternativi, ham rad etildi)
