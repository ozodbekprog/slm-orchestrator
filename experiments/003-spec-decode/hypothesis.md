# Tajriba 003: Speculative Decoding — Gipoteza

## Gipoteza
Kichik draft model (Qwen2.5-0.5B) yordamida mutaxassis tezligini
+20-40% oshirish mumkin.

## Usul
```bash
llama-server -m math.gguf \
  --spec-draft-model draft-qwen05b-q4km.gguf \
  --spec-draft-ngl 99 --spec-draft-n-max 4
```

## Oldingi natijalar (boshqa loyiha)
| Test | Baseline | Spec-decode | Natija |
|---|---|---|---|
| Falcon3-10B | 8.2 tok/s | 6.55 tok/s | ❌ |
| Maple 20B-A1B | 65 tok/s | 56.9 tok/s | ❌ |
| Llama.cpp DSpark | — | llama.cpp porti yo'q | ❌ |

## Kutilma
1.5B mutaxassis + 0.5B draft: acceptance yaxshi bo'lishi mumkin
(draft kichik, target kichik).
