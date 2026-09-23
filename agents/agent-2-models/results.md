# Agent-2: Modellar — Natijalar

## Vazifa
5 mutaxassis modelni yuklash, sozlash, test qilish.

## Natijalar

| Mutaxassis | Model | Hajm | Tezlik | Holat |
|---|---|---|---|---|
| math | Qwen2.5-Math-1.5B Q4_K_M | 941M | 102 tok/s | ✅ |
| code | Qwen2.5-Coder-1.5B Q4_K_M | 1.1G | 102.6 tok/s | ✅ |
| chat | Qwen2.5-1.5B Q4_K_M | 1.1G | 102.6 tok/s | ✅ |
| image | Qwen2-VL-2B Q4_K_M + mmproj | 941M+677M | 101 tok/s | ✅ |
| uz | alloma-8B Q4 (community) | 4.6G | 12.4 tok/s | ⚠️ |

## Sifat testlari
- math: 3x+5=20 → to'g'ri qadamlar bilan ✅
- code: factorial funksiya → to'g'ri ✅
- chat: salom + fun fact ✅
- image: sintetik rasm (shakllar + "HELLO KRONOS 42") → to'g'ri, OCR ishladi ✅
- uz: "Toshkent" to'g'ri, lekin ba'zan glitch tokenlar (masalan "OAPST...") ⚠️

## Fayllar
- `models/{math,code,chat,image,uz}/*.gguf`
- `scripts/test_specialists.sh`, `scripts/test_image.sh`

## Saboqlar
1. Q4_K_M — yaxshi balans (sifat/tezlik/hajm)
2. alloma-8B 4.6GB → 4GB VRAM'ga sig'maydi (qismli offload, 12 tok/s)
3. Image model faqat **tushunadi**, generatsiya qilmaydi

## Keyingi Qadam
uz uchun yengilroq model (alloma-3B?) yoki yaxshiroq kvant
