# Router — Latency

## Gibrid router

| Yo'l | Latency | Ulush |
|---|---|---|
| Semantic (fast) | 18-29 ms (CPU) | ~66% |
| LoRA fallback | ~100 ms (CPU) | ~34% |
| **O'rtacha** | **17.6 ms** | |

## Komponentlar

| Bosqich | Device | Vaqt |
|---|---|---|
| Encoding (MiniLM) | CPU | 15-25 ms |
| Route matching (5×cosine) | CPU | <1 ms |
| LoRA forward (fallback) | CPU | ~80-100 ms |
| LoRA (oldingi o'lchov, GPU) | GPU | 35 ms |

## Eslatma
Router GPU'da 5-35ms bo'lardi, lekin 4GB VRAM to'liq mutaxassislarga
kerak → CPU qabul qilindi. CPU LoRA (~100ms) faqat 34% holatda ishlaydi.

## Warmup effekti
- Startup warmup bo'lmasa: birinchi LoRA chaqiruv **418 ms**
- Warmup bilan: birinchi chaqiruv ham ~100 ms
