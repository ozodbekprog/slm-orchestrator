# 01 — Arxitektura

## Umumiy oqim

```
                ┌─────────────────────────────────────┐
   Savol ──────>│         GIBRID ROUTER               │
                │  semantic (CPU, MiniLM) ~20ms       │
                │    score >= 0.5 → route             │
                │    score <  0.5 → LoRA (CPU) ~100ms │
                └──────────────┬──────────────────────┘
                               │ route ∈ {math, code, chat, image, uz}
                ┌──────────────▼──────────────────────┐
                │   Specialists Manager (LRU=1)       │
                │   llama-server lazy start           │
                └──────────────┬──────────────────────┘
       ┌────────┬──────────┬───┴────┬──────────┬────────┐
     math      code       chat    image       uz
     :8101     :8102      :8103   :8104      :8105
   1.5B Q4   1.5B Q4    1.5B Q4  2B+mmproj  8B Q4(ngl20)
   102 tok/s 102.6       102.6    101 tok/s   12.4 tok/s
```

## Router dizayni

| Qatlam | Model | Device | Latency | Aniqlik |
|---|---|---|---|---|
| Semantic | paraphrase-multilingual-MiniLM-L12-v2 (118M) | CPU | 18-29 ms | 92.1% |
| LoRA fallback | Qwen2.5-0.5B + LoRA r16/α32 | CPU | ~100 ms | 99.95% |
| **Gibrid** | threshold 0.5 | CPU | 17.6 ms (o'rt.) | **98.9%** |

**Nega ikkala komponent ham CPU'da?** 4GB VRAM to'liq mutaxassislarga
kerak. Router CPU'da 20-100ms — qabul qilinadi. (GPU'da bo'lsa 5-35ms
bo'lardi, lekin VRAM yetmaydi.)

## Mutaxassis boshqaruvi (LRU=1)

```
ensure_specialist(tag):
    agar aktiv == tag: qaytarish
    agar aktiv: o'chirish (SIGTERM)
    yangi llama-server ishga tushirish
    health kutish (120s gacha)
```

- Portlar: 8101-8105
- Flags: `-ngl 99` (to'liq GPU), uz: `-ngl 20 -ot emb/head=CPU`
- Swap vaqti: 5-20 s (disk yuklash)

## Xotira byudjeti

| Resurs | Hajm | Izoh |
|---|---|---|
| VRAM | 4096 MB | GTX 1650 |
| math/code/chat/image | ~1.1-1.7 GB | bittasi bir vaqtda |
| uz | ~3.2 GB | ngl 20 |
| RAM | 15 GB | mmap + page cache |

## API

| Endpoint | Tavsif |
|---|---|
| `GET /` | Chat UI (brauzer) |
| `GET /health` | Holat |
| `POST /route` | Faqat marshrut (fast) |
| `POST /ask` | Route + mutaxassis javobi |
| `GET /docs` | Swagger UI |
