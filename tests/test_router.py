#!/usr/bin/env python3
"""Router smoke testlari (semantic qism, modelsiz ishlaydi)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "router"))


def test_imports():
    from semantic_router_eval import CLASSES, UTTERANCES
    assert CLASSES == ["math", "code", "uz", "chat", "image"]
    for c in CLASSES:
        assert len(UTTERANCES[c]) >= 20, f"{c} utterancelari kam"


def test_utterances_quality():
    from semantic_router_eval import UTTERANCES
    all_utts = [u for lst in UTTERANCES.values() for u in lst]
    assert len(all_utts) == len(set(all_utts)), "dublikat utterance bor"


def test_thresholds_config():
    from hybrid_router_eval import THRESHOLDS
    assert 0.5 in THRESHOLDS


if __name__ == "__main__":
    test_imports()
    test_utterances_quality()
    test_thresholds_config()
    print("✅ Router testlari o'tdi")
