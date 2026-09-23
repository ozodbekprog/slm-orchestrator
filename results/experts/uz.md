# Uz mutaxassis — Natijalar

| | |
|---|---|
| Model | alloma-8B (community: `kmamaroziqov/alloma-8b-q4`) |
| Format | Q4_K_M (4.6G) |
| Port | 8105 |
| Tezlik | **12.4 tok/s** (ngl 20 qismli offload) |
| VRAM | ~3.2 GB |
| Sinf | ⚠️ eng muammoli |

## Sifat testlari
| Savol | Javob | Baho |
|---|---|---|
| "Poytaxti qayerda?" | "Ozbekistonning poytaxti - Toshkent." | ✅ (kichik glitch) |
| "Salom, qalaysiz?" | "Yaxshi rahmat." | ✅ |
| "Menga qisqa maslahat ber" | "KoAPSTproq mashq qiling." | ⚠️ glitch |
| "Ozbekistonning poytaxti?" (TQ2_0) | "BoundingBounding..." | ❌ arxiv |

## Muammolar
1. **Sekin**: 8B > 4GB VRAM → ngl 20 (qismli), CPU qismi 12 tok/s
2. **Glitch tokenlar**: "OAPST", "KoAPSTproq" — community kvant + qismli yuklash
3. **TQ2_0 sinovi**: gibberish (arxiv)

## Variantlar (kelajak)
- alloma-3B (agar GGUF chiqsa) — to'liq VRAM'ga sig'adi
- Uy sharoitida fine-tune (LoRA, o'zbek ma'lumotlari)
- Boshqa o'zbek modellari (uzlm/alloma yangi versiyalari)
