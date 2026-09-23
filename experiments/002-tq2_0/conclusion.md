# Tajriba 002: TQ2_0 — Xulosa

## Qaror: ❌ RAD ETILDI (sifat sababli)

1. **1.5B modellar**: gibberish + sekin (86 vs 102) → rad
2. **8B alloma**: gibberish (to'liq VRAM'ga sig'ardi +20.2 tok/s edi) → rad
3. Fayllar `models/_attic/` da saqlandi (4.9GB, o'chirilmadi — saboq uchun)

## Nima uchun?
- Post-hoc ternary (QAT'siz) og'irliklarni buzadi
- MATRIX-DTO tajribasi: 0.5B post-hoc → benchmark 0%
- Falcon3-1.58bit/BitNet/Maple QAT bilan o'qitilgan — ular ishlaydi

## Agar shrink kerak bo'lsa
- Nativ ternary modellar tanlash (chat uchun Falcon3-1B-1.58bit)
- Yoki QAT o'qitish (katta loyiha, alohida tadqiqot)
