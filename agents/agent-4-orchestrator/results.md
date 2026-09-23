# Agent-4: Orchestrator — Natijalar

## Vazifa
FastAPI orchestrator: router + mutaxassis menejeri + API.

## Natijalar

### API
| Endpoint | Tavsif | Holat |
|---|---|---|
| `GET /` | Chat UI (dark theme) | ✅ |
| `GET /health` | Holat | ✅ |
| `POST /route` | Faqat marshrut | ✅ |
| `POST /ask` | Route + javob | ✅ |
| `GET /docs` | Swagger UI | ✅ |

### Arxitektura
- LRU=1 lazy loading (4GB VRAM cheklovi)
- Startup warmup (418ms→100ms)
- Portlar: 8101-8105
- Router CPU'da (encoder + LoRA)

### E2E natijalar
| Savol | Route | tok/s | E2E |
|---|---|---:|---:|
| What is 2+2? | math | 92.7 | 2.3s |
| Say hello... | chat | 82.0 | 3.3s |
| Salom, qalaysiz? | uz | 5.7 | 6.3s |

## Topilgan muammolar va yechimlar
1. Adapter num_labels xatosi → qo'lda 5
2. pad_token yo'q → eos
3. SentenceTransformer GPU'ni egallardi → `encoder_device="cpu"`
4. Eski jarayon portni ushlab qolardi → tekshirish tartibi

## Fayllar
- `src/orchestrator/app.py`

## Keyingi Qadam
Batching n=2 + streaming
