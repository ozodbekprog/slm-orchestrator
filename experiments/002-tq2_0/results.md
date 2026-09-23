# Tajriba 002: TQ2_0 — Natijalar

## Konversiya (llama-quantize, 2-10 soniya)

| Model | Q4_K_M | TQ2_0 | Farq |
|---|---|---|---|
| math 1.5B | 941M | 565M (3.04 bpw) | -40% |
| code 1.5B | 1.12G | 802M (3.76 bpw) | -28% |
| chat 1.5B | 1.12G | 802M | -28% |
| uz 8B | 4.6G | 2.8G (2.91 bpw) | -39% |

## Tezlik (Vulkan tg32)

| Model | Q4_K_M | TQ2_0 | Natija |
|---|---:|---:|---|
| math | 102.4 | 86.6 | ❌ -15% |
| code | 101.3 | 85.9 | ❌ |
| chat | 101.4 | 85.9 | ❌ |
| uz (ngl20→ngl99) | 12.4 | **20.2** | ✅ +64% |

## Sifat (haqiqiy testlar)

| Model | So'rov | Javob | Baho |
|---|---|---|---|
| math-tq2 | "Solve 3x+5=20" | `values dozen xf..率为 resultanna g...` | ❌ gibberish |
| uz-tq2 | "Poytaxti qayerda?" | `BoundingBoundingBounding...` | ❌ gibberish |
| math Q4 | xuddi shu | to'g'ri qadamlar | ✅ |
| uz Q4 | xuddi shu | "Toshkent" | ✅ |

## Xulosa
Format ishlaydi, lekin **post-hoc ternary modelni buzadi** (QAT yo'q).
Vulkan TQ2_0 shader ham Q4_K_M MMQ'dan samarasiz (kichik model sekin).

## Fayllar
- `models/_attic/*-tq2_0.gguf` (arxiv, 4.9GB)
