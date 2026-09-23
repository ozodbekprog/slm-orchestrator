# Tajriba 001: SASORI — Natijalar

## Tekshiruv

| Da'vo | Tekshiruv usuli | Natija |
|---|---|---|
| Konvertor mavjud | HF repo fayllari | ❌ Faqat 2 tayyor GGUF + binary runtime |
| 11GB → 1.4GB | bpw hisobi: 6.19 bpw × 14.5B / 8 | ❌ ≈11GB (o'zgarmaydi) |
| 217 tok/s | Muallif model card | ❌ 1.7-5.8 tok/s (14B, 8-yadro) |
| Zero-skip | Model card: "dense maddubs, no zero-skipping" | ❌ Yo'q |
| Format | Custom ggml type id 43, patch yopiq | ⚠️ Integratsiya imkonsiz |

## O'lchangan (qo'shimcha)
- TQ3P = quality-per-bit format (K=1 yiqiladi, K=3 sifat qaytadi)
- Q4_K_M'dan KATTA va sekinroq

## Fayllar
- Bu tajriba uchun kod yozilmadi (feasibility bosqichida rad etildi)
