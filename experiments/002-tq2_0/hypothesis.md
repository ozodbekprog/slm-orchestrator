# Tajriba 002: TQ2_0 Post-hoc Kvantlash — Gipoteza

## Gipoteza
Mavjud Q4_K_M modellarni TQ2_0 (2.06 bpw) formatga o'tkazib:
- Hajm 30-60% kamayadi
- Tezlik oshadi (kamroq bayt o'qish)

## Usul
```bash
llama-quantize --allow-requantize \
  --token-embedding-type q8_0 --output-tensor-type q8_0 \
  model.gguf model-tq2_0.gguf TQ2_0
```

## Kutilayotgan Natija
| Model | Q4 hajm | TQ2_0 hajm | Tezlik |
|---|---|---|---|
| 1.5B | 1.12G | ~0.5G | +50% |
| 8B | 4.6G | ~2.0G | to'liq VRAM'ga sig'adi |
