# Image mutaxassis — Natijalar

| | |
|---|---|
| Model | Qwen2-VL-2B-Instruct |
| Format | Q4_K_M (941M) + mmproj Q8_0 (677M) |
| Port | 8104 |
| Tezlik | **101.0 tok/s** (matn yo'li) |
| VRAM | ~1.7 GB |

## Sifat testi (sintetik rasm)
Rasm: ko'k to'rtburchak (chap), qizil doira (o'ng), "HELLO KRONOS 42" matni.

**Javob:** *"The image contains two shapes: a blue rectangle and a red
circle... some text at the bottom that says **HELLO KRONOS 42**"* ✅

- Shakllar to'g'ri aniqlandi ✅
- Ranglar to'g'ri ✅
- **OCR ishladi** (matnni o'qidi) ✅

## Muhim cheklov
Bu model rasmni **TUSHUNadi** (VQA, OCR, tavsif), lekin **generatsiya
qilmaydi**. Router "image" sinfidagi "draw a cat" so'rovlari uchun
alohida diffuzion model kerak (kelajak ishi).

## Test skripti
`scripts/test_image.sh` (sintetik rasm + base64 API)
