#!/usr/bin/env python3
"""SLM Orkestrator — router/predict.py

Gibrid router: semantic (CPU, tez) + LoRA (GPU, zaxira, threshold < 0.5).

Foydalanish:
    .venv/bin/python src/router/predict.py "Solve 3x + 5 = 20"
    .venv/bin/python src/router/predict.py --tests     # 20 ta real savol testi
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import torch
from peft import PeftModel
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer

sys.path.insert(0, str(Path(__file__).parent))
from semantic_router_eval import CLASSES, ENCODER, UTTERANCES  # noqa: E402

ADAPTER = Path(__file__).resolve().parents[2] / "models" / "router" / "lora_adapter"
BASE = "models/qwen2.5-0.5b-instruct"

TEST_QUESTIONS: list[tuple[str, str]] = [
    ("Solve 3x + 5 = 20", "math"),
    ("What is the integral of sin(x)?", "math"),
    ("5! nechaga teng?", "uz"),
    ("What is 15% of 240?", "math"),
    ("My Flask app returns a 500 error on POST requests", "code"),
    ("Write a Python function to merge two sorted lists", "code"),
    ("Write a SQL query to find the top customers", "code"),
    ("Can you explain the difference between TCP and UDP?", "code"),
    ("Bu kodda xato bormi? def add(a,b): return a-b", "uz"),
    ("O'zbekistonning poytaxti qayerda?", "uz"),
    ("Menga yaxshi kitob tavsiya qiling", "uz"),
    ("Salom, qalaysiz?", "uz"),
    ("Bugun kayfiyatim yaxshi, suhbatlashamizmi?", "uz"),
    ("I feel tired today, any tips?", "chat"),
    ("Hello! How are you?", "chat"),
    ("What's the weather like in Tashkent tomorrow?", "chat"),
    ("Draw a futuristic car in neon style", "image"),
    ("Remove the background from this photo", "image"),
    ("Generate a logo for my bakery", "image"),
    ("Turn this sketch into a 3D render", "image"),
]


class RouterPredictor:
    def __init__(self, threshold: float = 0.5, use_lora: bool = True,
                 lora_device: str | None = None, encoder_device: str | None = None):
        self.threshold = threshold
        self.encoder_device = encoder_device or ("cpu" if torch.cuda.is_available() else "cpu")
        print(f"Semantic encoder ({self.encoder_device})...")
        self.st = SentenceTransformer(ENCODER, device=self.encoder_device)
        self.route_embs = {
            r: self.st.encode(u, normalize_embeddings=True, convert_to_numpy=True,
                              show_progress_bar=False)
            for r, u in UTTERANCES.items()
        }
        self.lora = self.tok = None
        if use_lora:
            dev = lora_device or ("cuda" if torch.cuda.is_available() else "cpu")
            print(f"LoRA router ({dev})...")
            base = AutoModelForSequenceClassification.from_pretrained(
                BASE, num_labels=5, torch_dtype=torch.float32)
            self.lora = PeftModel.from_pretrained(base, str(ADAPTER)).to(dev)
            self.lora.eval()
            self.tok = AutoTokenizer.from_pretrained(str(ADAPTER))
            if self.tok.pad_token is None:
                self.tok.pad_token = self.tok.eos_token
            self.lora.config.pad_token_id = self.tok.pad_token_id
            self.dev = dev

    def _lora_predict(self, text: str) -> str:
        enc = self.tok([text], padding=True, truncation=True, max_length=64,
                       return_tensors="pt").to(self.dev)
        with torch.no_grad():
            idx = int(self.lora(**enc).logits.argmax(-1).item())
        return CLASSES[idx]

    def predict(self, text: str) -> dict:
        t0 = time.perf_counter()
        emb = self.st.encode([text], normalize_embeddings=True, convert_to_numpy=True,
                             show_progress_bar=False)[0]
        best, score = "chat", -1.0
        for r in CLASSES:
            s = float(np.max(emb @ self.route_embs[r].T))
            if s > score:
                best, score = r, s
        if score >= self.threshold:
            route, source = best, "semantic"
        else:
            route, source = self._lora_predict(text), "lora"
        return {"route": route, "score": round(score, 3), "source": source,
                "latency_ms": round((time.perf_counter() - t0) * 1000, 1)}


def run_tests(router: RouterPredictor) -> None:
    print(f"\n{'#':>2s} {'savol':52s} {'kutilgan':>8s} {'topildi':>8s} "
          f"{'manba':>8s} {'score':>6s} {'ms':>6s} {'OK':>3s}")
    print("-" * 105)
    n_ok = 0
    total_lat = 0.0
    for i, (q, expected) in enumerate(TEST_QUESTIONS, 1):
        r = router.predict(q)
        ok = r["route"] == expected
        n_ok += ok
        total_lat += r["latency_ms"]
        print(f"{i:>2d} {q[:52]:52s} {expected:>8s} {r['route']:>8s} "
              f"{r['source']:>8s} {r['score']:>6.3f} {r['latency_ms']:>6.1f} "
              f"{'✅' if ok else '❌'}")
    print("-" * 105)
    print(f"Aniqlik: {n_ok}/{len(TEST_QUESTIONS)} = {100*n_ok/len(TEST_QUESTIONS):.1f}% | "
          f"o'rtacha latency: {total_lat/len(TEST_QUESTIONS):.1f} ms")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query", nargs="?", help="bitta savol")
    ap.add_argument("--tests", action="store_true", help="20 ta test savol")
    ap.add_argument("--threshold", type=float, default=0.5)
    args = ap.parse_args()

    router = RouterPredictor(threshold=args.threshold)
    if args.tests or not args.query:
        run_tests(router)
    else:
        r = router.predict(args.query)
        print(f"\nSavol   : {args.query}")
        print(f"Route   : {r['route']}")
        print(f"Manba   : {r['source']} (score={r['score']}, threshold={args.threshold})")
        print(f"Latency : {r['latency_ms']} ms")


if __name__ == "__main__":
    main()
