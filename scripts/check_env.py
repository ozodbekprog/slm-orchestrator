#!/usr/bin/env python3
"""SLM Orkestrator — muhit auditi (BOSQICH 1)."""
from __future__ import annotations

import importlib
import platform
import shutil
import sys

REQUIRED = {
    "torch": "PyTorch (CUDA)",
    "transformers": "HF transformers",
    "peft": "LoRA",
    "datasets": "datasetlar",
    "accelerate": "training",
}
OPTIONAL = {
    "sklearn": "confusion matrix / F1",
    "matplotlib": "grafiklar",
    "onnx": "export (5-bosqich)",
    "onnxruntime": "ONNX inference",
}


def check(pkgs: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    ok, missing = {}, []
    for mod, label in pkgs.items():
        try:
            m = importlib.import_module(mod)
            ok[mod] = getattr(m, "__version__", "?")
        except Exception:
            missing.append(f"{mod} ({label})")
    return ok, missing


def main() -> None:
    print("=" * 60)
    print("SLM ORKESTRATOR — MUHIT AUDITI")
    print("=" * 60)
    print(f"Python     : {sys.version.split()[0]}")
    print(f"Platform   : {platform.platform()}")
    print(f"nvcc       : {shutil.which('nvcc') or 'YO`Q (llama.cpp CUDA build uchun kerak)'}")
    print(f"cmake      : {shutil.which('cmake') or 'yo`q'}")

    ok, missing = check(REQUIRED)
    print("\n[Asosiy paketlar]")
    for mod, ver in ok.items():
        print(f"  ✓ {mod:14s} {ver}")
    for m in missing:
        print(f"  ✗ {m}")

    ok_opt, missing_opt = check(OPTIONAL)
    print("\n[Ixtiyoriy paketlar]")
    for mod, ver in ok_opt.items():
        print(f"  ✓ {mod:14s} {ver}")
    for m in missing_opt:
        print(f"  - {m}")

    print("\n[GPU]")
    try:
        import torch

        if torch.cuda.is_available():
            p = torch.cuda.get_device_properties(0)
            print(f"  GPU   : {p.name}")
            print(f"  VRAM  : {p.total_memory / 2**30:.2f} GiB")
            print(f"  sm    : {p.major}.{p.minor}")
            print("  ⚠ fp16 matmul bu kartada sekin (o'lchangan: 315 GFLOPS vs fp32 1484)")
            print("  → Router o'qitish fp32 + gradient accumulation bilan")
        else:
            print("  CUDA mavjud emas!")
    except Exception as e:
        print(f"  torch xatosi: {e}")

    print("\n[Ma'lumotlar]")
    from pathlib import Path

    for p in ["data", "router", "specialists", "logs"]:
        print(f"  {'✓' if Path(p).is_dir() else '✗'} {p}/")
    uz = Path("../uz-llm-lab/data/uzbek-instruct.jsonl")
    print(f"  {'✓' if uz.exists() else '✗'} uz 'uz' sinfi uchun: {uz}")

    if missing:
        print("\nO'rnatish: .venv/bin/pip install " + " ".join(m.split()[0] for m in missing))
        sys.exit(1)
    print("\nNATIJA: Barcha asosiy paketlar tayyor ✅")


if __name__ == "__main__":
    main()
