# Tajriba 003: Spec-Decode — Natijalar

## Holat: ⏳ QISMAN (mutaxassislarda sinlanmagan)

### Oldingi loyihalarda (o'lchangan)
| Setup | Baseline | Spec-decode | Xulosa |
|---|---|---|---|
| Falcon3-10B + draft | 8.2 | 6.55 | ❌ -20% |
| Maple 20B-A1B + Qwen0.5B | 65.0 | 56.9 | ❌ -12% |

### Sabablari
1. Draft model forward'lari qo'shimcha vaqt oladi
2. Acceptance reasoning matnida past
3. Target verify pass arzon emas (MoE/dense)

### 1.5B mutaxassislar uchun prognoz
- Target: 1.5B Q4 (~660ms/64 token)
- Draft: 0.5B Q4 (~200ms/4 token + verify)
- Kuzatilishi kerak: acceptance rate

## DSpark izohi
- DeepSeek'ning usuli; portlar faqat MLX/vLLM/SGLang da
- llama.cpp porti YO'Q → bizda ishlamaydi

## Keyingi qadam
`llama-bench` draft flaglarini qo'llab-quvvatlamaydi;
server orqali test qilish kerak (acceptance metrikasi bilan).
