# 04 — Qarorlar Tarixi (ADR)

## 2026-09-20: Python 3.12 (3.10 emas)
- **Kontekst:** Python 3.10 talab qilingan edi
- **Qaror:** 3.12.14 ishlatildi
- **Sabab:** 3.10 o'rnatilmagan; torch 2.14 3.12 bilan to'liq mos
- **Natija:** ✅ Muammosiz

## 2026-09-20: Mavjud venv (yangi emas)
- **Qaror:** `uz-llm-lab/.venv` ga symlink
- **Sabab:** yangi venv ~6GB yuklab olish (tarmoq sekin); barcha paketlar bor
- **Natija:** ✅ Vaqt tejaldi

## 2026-09-20: fp32 o'qitish (fp16 emas)
- **Kontekst:** fp16 tavsiya etilgan edi
- **Qaror:** fp32
- **Sabab:** O'lchandi: bu GPU'da fp16 **315** vs fp32 **1484** GFLOPS (5x sekin)
- **Natija:** ✅ LoRA 21.6 daqiqada o'qitildi

## 2026-09-20: llama.cpp Vulkan (CUDA emas)
- **Qaror:** Vulkan backend
- **Sabab:** nvcc (CUDA toolkit) yo'q; Vulkan build ishlaydi (GTX 1650)
- **Natija:** ✅ 101-103 tok/s

## 2026-09-22: Gibrid router (semantic + LoRA)
- **Qaror:** semantic asosiy + LoRA fallback (threshold 0.5)
- **Sabab:** semantic 92.1% (til chegarasida xato), LoRA 99.95% (lekin sekin)
- **Natija:** ✅ 98.9%, 17.6 ms

## 2026-09-23: Router CPU'ga (VRAM uchun)
- **Kontekst:** SentenceTransformer ham GPU'ni egallardi
- **Qaror:** encoder + LoRA ikkalasi CPU
- **Sabab:** 4GB VRAM to'liq mutaxassislarga kerak; CPU 20-100ms qabul qilinadi
- **Natija:** ✅ uz yuklanadi, router ishlaydi

## 2026-09-23: SASORI rad etildi
- **Qaror:** SASORI ishlatilmaydi
- **Sabab:** konvertor yo'q, TQ3P=6.19bpw (Q4'dan katta), muallif o'lchovi sekin
- **Alternativa:** nativ ternary modellar (Falcon3-1.58bit) yoki QAT

## 2026-09-23: TQ2_0 rad etildi
- **Qaror:** post-hoc TQ2_0 ishlatilmaydi
- **Sabab:** 1.5B va 8B ikkalasida ham gibberish; sekinroq (86 vs 102 tok/s)
- **Saboq:** ternary faqat QAT o'qitilgan modellarda ishlaydi

## 2026-09-23: LRU=1 mutaxassis boshqaruvi
- **Qaror:** bir vaqtda 1 llama-server
- **Sabab:** 4GB VRAM — uz (3.2GB) + boshqa model sig'maydi
- **Natija:** ⚠️ almashish 5-20s (arxitektura cheklovi)
