# Code mutaxassis — Natijalar

| | |
|---|---|
| Model | Qwen2.5-Coder-1.5B-Instruct |
| Format | Q4_K_M (1.04 GiB) |
| Port | 8102 |
| Tezlik | **102.6 tok/s** (pp64=1008) |
| VRAM | ~1.2 GB |

## Sifat testlari
| Savol | Javob | Baho |
|---|---|---|
| "factorial function" | to'g'ri Python kod | ✅ |
| "reverse string one-liner" | `string[::-1]` | ✅ |
| "merge sorted lists" | to'g'ri | ✅ |
| "SQL top customers" | to'g'ri so'rov | ✅ |
| "TCP vs UDP" | tushuntirish | ✅ |

## Eslatma
Kod javoblarni markdown kod blokida beradi.
Vulkan build'da code sinfiga TEZ javob (102 tok/s).
