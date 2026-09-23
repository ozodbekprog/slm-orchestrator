# Agent-5: Meta-Learner — Reja (bajarilmagan)

## Vazifa
Router ishonchi past bo'lganda javob sifatini oshirish.

## Rejalashtirilgan yondashuv

```
query → router → p(route)
         │
         ├─ p >= 0.7  → bitta mutaxassis
         ├─ 0.5-0.7   → 2 mutaxassis javobini solishtirish (self-consistency)
         └─ p < 0.5   → chat mutaxassisga fallback yoki foydalanuvchidan aniqlashtirish
```

## Variantlar
1. **Self-consistency**: 2-3 mutaxassis javobini olib, eng ishonchlisini tanlash
2. **Confidence calibration**: router ehtimolini kalibrlash (temperature scaling)
3. **Feedback loop**: foydalanuvchi javoblaridan o'rganish (keyinroq)

## Kerakli resurslar
- Router logits (hozir faqat route qaytadi)
- Qo'shimcha VRAM yoki navbat (LRU) — 4GB cheklovi
- Evaluatsiya to'plami

## Holat
⏳ Rejalashtirilgan (ROADMAP #6)

## Fayllar (kelajakda)
- `src/meta_learner/` (bo'sh hozircha)
