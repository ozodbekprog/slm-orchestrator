# Agent-1: Router — Natijalar

## Vazifa
Savolni to'g'ri mutaxassisga yo'naltiruvchi router qurish.

## Natijalar

### Semantic Router
- Aniqlik: **92.1%**, latency 18-29 ms (CPU)
- O'qitish: ❌ kerak emas
- Muammo: chat↔uz til chegarasi

### LoRA Router
- Aniqlik: **99.95%**, latency ~100 ms (CPU)
- O'qitish: ✅ 21.6 daqiqa (Qwen2.5-0.5B, r16/α32, fp32)
- Eval: 1999/2000 (1 xato: uz→chat)

### Gibrid Router ✅
- Aniqlik: **98.9%**, latency 17.6 ms (threshold 0.5)
- Thresholdlar: 0.40→95.3%, 0.50→98.9%, 0.55→99.65%, 0.60→99.75%

### Real savollar (20 ta)
- 19/20 = **95%** (xato: "Bu kodda xato bormi? def add..." → code, kutilgan uz)

## Fayllar
- `src/router/semantic_router_eval.py`
- `src/router/hybrid_router_eval.py`
- `src/router/predict.py`
- `src/router/train_router.py`
- `logs/inference/hybrid_router_results.json`

## Saboqlar
1. Multilingual encoder tarjimalarni yaqinlashtiradi (til ≠ semantika)
2. LoRA til chegarasini hal qiladi
3. Gibrid = tezlik + aniqlik muvozanati

## Keyingi Qadam
Threshold tuning yoki dataset'ga hard-negative qo'shish
