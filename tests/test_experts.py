#!/usr/bin/env python3
"""Mutaxassis fayllari mavjudligini tekshirish (modelsiz)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"

REQUIRED = {
    "math": MODELS / "math" / "math.gguf",
    "code": MODELS / "code" / "code.gguf",
    "chat": MODELS / "chat" / "chat.gguf",
    "image": MODELS / "image" / "image.gguf",
    "image_mmproj": MODELS / "image" / "mmproj.gguf",
    "uz": MODELS / "uz" / "uz.gguf",
}


def test_files_exist():
    missing = [k for k, p in REQUIRED.items() if not p.exists()]
    assert not missing, f"Yetishmayapti: {missing}"


def test_file_sizes():
    for k, p in REQUIRED.items():
        if p.exists():
            assert p.stat().st_size > 100_000_000, f"{k} juda kichik (buzilgan?)"


def test_router_adapter():
    adapter = MODELS / "router" / "lora_adapter" / "adapter_model.safetensors"
    assert adapter.exists(), "LoRA adapter yo'q — train_router.sh ishga tushiring"


if __name__ == "__main__":
    test_files_exist()
    test_file_sizes()
    test_router_adapter()
    print("✅ Mutaxassis fayllari testi o'tdi")
