# Router — Aniqlik

## Gibrid router (threshold 0.5), eval: 2000 namuna

| Metrika | Qiymat |
|---|---|
| Accuracy | **98.90%** |
| F1 macro | 98.9% |
| Fallback rate | 34.0% |

## Threshold taqqoslash

| Threshold | Accuracy | Fallback | Izoh |
|---:|---:|---:|---|
| 0.40 | 95.30% | 11.8% | tez, xatolar ko'p |
| 0.45 | 97.20% | 22.6% | |
| **0.50** | **98.90%** | **34.0%** | ✅ tanlangan |
| 0.55 | 99.65% | 45.5% | sekin |
| 0.60 | 99.75% | 58.4% | juda sekin |

## Sof komponentlar

| Router | Accuracy |
|---|---|
| Semantic | 92.10% |
| LoRA | 99.95% (1 xato / 2000) |

## Real savollar (20 ta)
19/20 = 95%. Xato:
`"Bu kodda xato bormi? def add(a,b): return a-b"` → code (kutilgan uz)
— label dizayni: o'zbekcha savol, lekin kod mazmuni.

## Confusion matrix (thr 0.6, eval)
```
        math  code   uz  chat image
math     400     0    0     0    0
code       0   400    0     0    0
uz         1     0  396     2    1
chat       0     0    1   399    0
image      0     0    0     0  400
```

To'liq JSON: `logs/inference/hybrid_router_results.json`
