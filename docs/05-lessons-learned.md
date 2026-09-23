# 05 — Saboqlar (Lessons Learned)

## 1. Post-hoc ternary kvantlash ishlamaydi
TQ2_0 ga o'tkazilgan modellar (1.5B va 8B) **gibberish** chiqardi.
Bu MATRIX-DTO tajribasini tasdiqlaydi: ternary sifat faqat **QAT yoki
nativ ternary o'qitilgan** modellarda saqlanadi (Falcon3-1.58bit, BitNet).

## 2. Multilingual encoder til chegarasini "ko'rmaydi"
"hello" va "salom" embedding fazosida yaqin — chunki model tarjimalarni
yaqinlashtiradi. Natija: chat ↔ uz chalkashligi. Yechim: LoRA fallback
yoki til-detektor (lekin soddalashtirilgan detektor xavfli — `-ing` suffix
ingliz so'zlarini o'zbekcha deb belgilagan edi).

## 3. VRAM 4GB — qattiq cheklov
Router GPU'da (2GB) + uz (3.2GB) = sig'maydi. Yechim: routerni CPU'ga.
Har bir GB VRAM uchun kurash kerak.

## 4. Kernel samaradorligi formatdan muhim
TQ2_0 Q4_K_M'dan 30% kichik, lekin **15% sekin** — chunki Vulkan TQ2_0
shaderi MMQ yo'lidan samarasiz. Kichikroq ≠ tezroq.

## 5. fp16 bu GPU'da tuzoq
GTX 1650'da fp16 matmul fp32'dan 5x sekin (o'lchandi). "Standart"
tanlovlarni har doim o'lchash kerak.

## 6. Batching chegarasi bor
n=2 da 124.6 tok/s peak, lekin n=4/8 da tushadi (83/75). Sabab: contention
va per-step overhead. Ko'r-ko'rona parallelizm foyda bermaydi.

## 7. Fon jarayonlari VRAM'ni ushlab qoladi
Orphan llama-server/orchestrator jarayonlari yangi ishga tushishni buzadi
("address already in use", CUDA OOM). Har doim tekshirish kerak:
`pgrep -af "llama|uvicorn"`.

## 8. Ochiq format = tez yechim
I2_S → TQ2_0 transkoder 30 soniyada yozildi chunki formatlar manbadan
o'rganildi. Yopiq format (SASORI) esa umuman ishlamadi.

## 9. Sozlamalarni o'lchash kerak
- `-ngl 24` OOM, `-ngl 20` ishlaydi (alloma)
- `-ngl 6/7` OOM (Maple misolida)
- Chegarani empirik topish kerak

## 10. Hujjatlashtirmaslik = yo'qotish
Natijalar tarqalib ketsa (loglar, chatlar, kodlar) — qarorlar qayta
qabul qilinadi. Har bir tajriba hypothesis/results/conclusion bilan
saqlanishi kerak.
