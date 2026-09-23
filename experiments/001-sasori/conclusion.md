# Tajriba 001: SASORI — Xulosa

## Qaror: ❌ RAD ETILDI

SASORI bizning maqsadlarimiz uchun yaroqsiz:
1. Konvertor/source ochiq emas (integratsiya imkonsiz)
2. Format Q4_K_M'dan katta (6.19 bpw vs 4.5)
3. Muallif o'zi sekin deb o'lchagan
4. Zero-skip yo'q

## Alternativa
- Nativ ternary modellar (Falcon3-1.58bit, BitNet) — ishlaydi
- QAT o'qitish (MATRIX-DTO tajribasi) — uzoq muddatli yo'l

## Saboq
Ternary sifat faqat **QAT o'qitilgan** modellarda bo'ladi.
Post-hoc kvantlash (TQ2_0 sinovi ham) modelni buzadi.
