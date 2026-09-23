# O'zgarishlar Tarixi

## [2026-09-23] — KUN 4: Diagnostika + Tartibga Solish

### Qo'shildi
- To'liq loyiha strukturasi (docs/, daily/, agents/, experiments/, results/, src/, configs/, tests/)
- Barcha hujjatlar (README, STATUS, CHANGELOG, ROADMAP, docs/00-07)
- Chat UI orchestratorga (`GET /`)

### Tekshirildi (diagnostika)
- SASORI: ❌ yaroqsiz (yopiq, 6.19 bpw, sekin)
- TQ2_0 post-hoc: ❌ gibberish (1.5B va 8B ikkalasida)
- Batching: n=2 optimal (124.6 tok/s aggregate)
- Router: 5/5 real savolda to'g'ri

### Tuzatildi
- "Say hello in one sentence" routing xatosi (uz→chat): 12 ta utterance qo'shildi
- SentenceTransformer GPU'ni egallashi: `encoder_device="cpu"`
- Orphan jarayonlar tozalandi
- Fayllar tartibga solindi (models/*, src/*, logs/*)

### O'zgartirildi
- LoRA router GPU → CPU (VRAM mutaxassislarga)
- uz: `-ngl 20` qismli offload

## [2026-09-22] — KUN 3: Gibrid router + Orchestrator

### Qo'shildi
- Gibrid router (semantic + LoRA fallback, threshold 0.5)
- Orchestrator kodi (FastAPI, LRU=1 lazy loading, startup warmup)
- Chat UI

### Natijalar
- LoRA router: 99.95% aniqlik (21.6 daqiqa o'qitish)
- Gibrid: 98.9% aniqlik, 17.6 ms
- E2E: math 95 tok/s, 3/3 test

## [2026-09-21] — KUN 2: Semantic router + Dataset

### Qo'shildi
- Router dataset generator (10k namuna, 5 sinf; multiprocessing)
- Semantic router (multilingual MiniLM, 92.1%)

### Natijalar
- Dataset: 5×2000 (train 8000 / eval 2000)
- Semantic: 91.8% → 92.1% (utterance kengaytirish bilan)

## [2026-09-20] — KUN 1: Loyiha boshlanishi

### Qo'shildi
- Loyiha strukturasi + venv (Python 3.12, torch 2.14 CUDA)
- 5 mutaxassis model yuklab olindi (GGUF Q4_K_M)

### Qarorlar
- Python 3.10 yo'q → 3.12 ishlatildi
- fp16 bu GPU'da sekin → fp32 o'qitish
- nvcc yo'q → llama.cpp Vulkan backend

## [2026-09-23] — KUN 1 (optimizatsiya): SASORI tekshiruvi

### Tekshirildi
- SASORI: konvertor yo'q, TQ3P=6.19bpw (kattaroq), sekin → rad etildi
- TQ2_0 alternativi: kichraytiradi lekin sifatni buzadi → rad etildi
- Zero-skip PR #23439: CPU kernel uchun, GPU-bound da foyda yo'q
- MTP: bu modellarda yo'q (qo'shib bo'lmaydi)
