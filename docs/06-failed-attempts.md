# 06 — Muvaffaqiyatsiz Urinishlar (arxiv, saboq uchun)

## 1. SASORI ternary (2026-09-23)
- **Gipoteza:** 8x siqish, 217 tok/s
- **Natija:** ❌ Yaroqsiz
- **Sabab:** Konvertor/source yo'q (faqat binary runtime); TQ3P=6.19 bpw
  (Q4_K_M'dan katta); muallif o'lchovi 1.7-5.8 tok/s; zero-skip yo'q
- **Saboq:** Yopiq format + marketing raqamlarini tekshirmaslik kerak

## 2. TQ2_0 post-hoc kvantlash (2026-09-23)
- **Gipoteza:** 30-60% kichraytirish, tezlik oshadi
- **Natija:** ❌ Gibberish (1.5B math, 8B alloma); tezlik tushdi (86 vs 102)
- **Sabab:** QAT'siz ternary; Vulkan TQ2_0 shader samarasiz
- **Saboq:** Faqat nativ ternary modellar yoki QAT o'qitish

## 3. Soddalashtirilgan uz-detektor (2026-09-23)
- **Gipoteza:** suffix/so'z evristikasi tilni ajratadi
- **Natija:** ❌ 81.2% (semantic 92.1% dan yomon)
- **Sabab:** `-ing` suffix ingliz so'zlarini ("reading", "something") o'zbekcha deb belgiladi
- **Saboq:** Sodda til-detektor xavfli; LoRA fallback yaxshiroq

## 4. Zero-Skip PR #23439 (rejada edi)
- **Gipoteza:** +20-30% tezlik
- **Real:** PR faqat **d==0 bloklarni** skip qiladi (12 satr); CPU kernel;
  bizning yuk GPU-bound → ~0-2%
- **Saboq:** Kernel qayerda ishlaydi — tekshirish kerak

## 5. MTP (multi-token prediction)
- **Gipoteza:** +50% tezlik
- **Real:** ❌ Qwen2.5 modellarida MTP head **yo'q**; qo'shib bo'lmaydi
  (o'qitish kerak — modelni qayta o'qitish demakdir)
- **Saboq:** MTP faqat MTP bilan o'qitilgan modellarda (DeepSeek)

## 6. Spec-decode (Falcon3-10B, oldingi loyiha)
- **Gipoteza:** +50%
- **Natija:** ❌ 6.55 vs 8.2 tok/s (sekinlashtirdi)
- **Sabab:** katta model + zaif draft = overhead

## 7. Spec-decode (Maple 20B-A1B, oldingi loyiha)
- **Natija:** ❌ 56.9 vs 65 tok/s
- **Sabab:** reasoning matnida acceptance past
- **Saboq:** Draft model target bilan "mos" bo'lishi kerak

## 8. KroneckerBERT (oldingi loyiha, KRONOS)
- **Gipoteza:** 19x siqish
- **Natija:** ❌ SVD har doim yutadi (probe o'lchovi)
- **Saboq:** 19x — BERT+KD uchun; LLM post-hoc uchun yaroqsiz

## 9. Ikkala GPU split (KRONOS)
- **Natija:** ❌ OOM (Intel iGPU + NVIDIA birgalikda)
- **Saboq:** Vulkan multi-device split bu buildda barqaror emas
