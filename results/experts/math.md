# Math mutaxassis — Natijalar

| | |
|---|---|
| Model | Qwen2.5-Math-1.5B-Instruct |
| Format | Q4_K_M (941M) |
| Port | 8101 |
| Tezlik | **102.0 tok/s** (tg16, pp64=966) |
| VRAM | ~1.1 GB |

## Sifat testlari
| Savol | Javob | Baho |
|---|---|---|
| "Solve 3x+5=20" | qadamlar bilan x=5 | ✅ |
| "What is 7*6?" | qadamlar bilan 42 | ✅ |
| "12*12" | to'g'ri | ✅ |
| "2+2" | qadamlar bilan | ✅ |

## Eslatma
Ba'zan "qadamlar bilan" uzun javob beradi (model xususiyati).
`max_tokens` cheklash yoki "answer briefly" bilan qisqartirish mumkin.
