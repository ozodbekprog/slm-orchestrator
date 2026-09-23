# Kelajak Rejasi (ROADMAP)

## Qisqa muddat (1 hafta)

| # | Vazifa | Kutilma | Holat |
|---|---|---|---|
| 1 | Spec-decode test: 1.5B mutaxassis + Qwen0.5B draft | +20-40%? | ⏳ |
| 2 | Batching n=2 orchestratorga (`--parallel 2`) | aggregate 125 tok/s | ⏳ |
| 3 | uz: alloma-3B sinash (tezroq, yengilroq) | 20-40 tok/s | ⏳ |
| 4 | systemd user service | reboot survivability | ⏳ |
| 5 | Threshold tuning (#9 uz-code edge case) | +0.5% | ⏳ |

## O'rta muddat (1 oy)

| # | Vazifa | Izoh |
|---|---|---|
| 6 | Meta-Learner: router ishonchi past bo'lsa 2 mutaxassis javobini solishtirish |
| 7 | Guardrails (configs/guardrails.yaml) |
| 8 | Streaming javoblar (TTFT ~100ms) |
| 9 | uz model sifatini yaxshilash (fine-tune yoki boshqa kvant) |
| 10 | Router real foydalanuvchi savollari bilan qayta o'qitish |

## Uzoq muddat

| # | Vazifa | Izoh |
|---|---|---|
| 11 | Nativ ternary mutaxassislar (Falcon3-1.58bit kabi) |
| 12 | QAT o'qitish quvuri (MATRIX-DTO tajribasi asosida) |
| 13 | Kattaroq model bilan solishtirish (GPT-4 class) |
| 14 | Web deployment (auth, rate limit) |

## Bajarilganlar (arxiv)

- ✅ Router (semantic + LoRA + gibrid)
- ✅ 5 mutaxassis integratsiya
- ✅ Orchestrator (FastAPI)
- ✅ Diagnostika tizimi
- ❌ SASORI/TQ2_0 (buzilgan)
- ❌ MTP (qo'llab-quvvatlanmaydi)
