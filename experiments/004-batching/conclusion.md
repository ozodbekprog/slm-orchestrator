# Tajriba 004: Batching — Xulosa

## Qaror: ✅ n=2 QABUL QILINDI

1. **Peak: n=2 = 124.6 tok/s aggregate** (single 60 → 2x)
2. 217 tok/s maqsad erishilmaydi (degradatsiya n=4 dan boshlanadi)
3. Orchestrator uchun `--parallel 2` tavsiya etiladi

## Keyingi qadam
- Orchestrator menejeriga `--parallel 2` qo'shish
- Ikki foydalanuvchi bir mutaxassisda ishlaganda foyda beradi
- LRU=1 bilan birga: parallel faqat bitta mutaxassis ichida ishlaydi

## Saboq
Parallelism ko'r-ko'rona emas — n=2 optimal nuqta o'lchov bilan topildi.
Har bir qo'shimcha slot overhead keltiradi (attention, scheduling).
