#!/usr/bin/env python3
"""SLM Orkestrator — QADAM 2: GIBRID ROUTER (semantic + LoRA fallback).

Mantiq:
    query -> semantic router (multilingual MiniLM, 13.7 ms)
             ├─ score >= threshold → shu route (tez yo'l)
             └─ score <  threshold → LoRA router (Qwen0.5B, ~35 ms) — zaxira

Thresholdlar solishtiriladi: 0.40 / 0.45 / 0.50 / 0.55 / 0.60.
Natija: logs/hybrid_router_results.json

Ishlatish:
    .venv/bin/python router/hybrid_router_eval.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from peft import PeftModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer

sys.path.insert(0, str(Path(__file__).parent))
from semantic_router_eval import CLASSES, ENCODER, UTTERANCES, load_eval  # noqa: E402

ADAPTER = "models/router/lora_adapter"
BASE = "models/qwen2.5-0.5b-instruct"
THRESHOLDS = [0.40, 0.45, 0.50, 0.55, 0.60]


def load_lora():
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    base = AutoModelForSequenceClassification.from_pretrained(
        BASE, num_labels=5, torch_dtype=torch.float32)
    model = PeftModel.from_pretrained(base, ADAPTER).to(dev)
    model.eval()
    tok = AutoTokenizer.from_pretrained(ADAPTER)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model.config.pad_token_id = tok.pad_token_id
    return model, tok, dev


def main() -> None:
    texts, labels = load_eval()
    print(f"Eval: {len(texts)} namuna")

    print("Semantic encoder...")
    st = SentenceTransformer(ENCODER)
    route_names = CLASSES
    route_embs = {r: st.encode(u, normalize_embeddings=True, convert_to_numpy=True,
                               show_progress_bar=False) for r, u in UTTERANCES.items()}

    print("LoRA router...")
    lora, tok, dev = load_lora()

    sem_pred, sem_score = [], []
    t_sem = []
    for text in texts:
        t0 = time.perf_counter()
        emb = st.encode([text], normalize_embeddings=True, convert_to_numpy=True,
                        show_progress_bar=False)[0]
        best, best_score = "chat", -1.0
        for r in route_names:
            s = float(np.max(emb @ route_embs[r].T))
            if s > best_score:
                best, best_score = r, s
        t_sem.append((time.perf_counter() - t0) * 1000)
        sem_pred.append(CLASSES.index(best))
        sem_score.append(best_score)
    sem_pred = np.array(sem_pred)
    sem_score = np.array(sem_score)
    acc_sem = accuracy_score(labels, sem_pred)
    print(f"\nSof semantic: acc={acc_sem:.4f} | median latency={np.median(t_sem):.1f} ms")

    print("LoRA barcha namunalarga (fallback zaxirasi)...")
    lora_pred = []
    with torch.no_grad():
        for i in range(0, len(texts), 64):
            batch = texts[i:i + 64]
            enc = tok(batch, padding=True, truncation=True, max_length=64,
                      return_tensors="pt").to(dev)
            logits = lora(**enc).logits
            lora_pred.extend(logits.argmax(-1).cpu().tolist())
    lora_pred = np.array(lora_pred)
    acc_lora = accuracy_score(labels, lora_pred)
    print(f"Sof LoRA: acc={acc_lora:.4f}")

    results = {
        "semantic": {"accuracy": round(acc_sem, 4), "latency_ms": round(float(np.median(t_sem)), 2)},
        "lora": {"accuracy": round(acc_lora, 4)},
    }
    print(f"\n{'thr':>5s} {'acc':>7s} {'fallback%':>9s} {'med_ms':>7s} {'p90_ms':>7s}")
    for thr in THRESHOLDS:
        preds, lat = [], []
        n_fb = 0
        for i, text in enumerate(texts):
            if sem_score[i] >= thr:
                pred = sem_pred[i]
                lat.append(t_sem[i])
            else:
                n_fb += 1
                t0 = time.perf_counter()
                enc = tok([text], padding=True, truncation=True, max_length=64,
                          return_tensors="pt").to(dev)
                with torch.no_grad():
                    pred = int(lora(**enc).logits.argmax(-1).item())
                lat.append(t_sem[i] + (time.perf_counter() - t0) * 1000)
            preds.append(pred)
        preds = np.array(preds)
        acc = accuracy_score(labels, preds)
        results[f"hybrid_{thr}"] = {
            "accuracy": round(acc, 4),
            "fallback_pct": round(100 * n_fb / len(texts), 1),
            "latency_median_ms": round(float(np.median(lat)), 2),
            "latency_p90_ms": round(float(np.percentile(lat, 90)), 2),
            "f1_macro": round(f1_score(labels, preds, average="macro"), 4),
        }
        print(f"{thr:>5.2f} {acc:>7.4f} {100*n_fb/len(texts):>8.1f}% "
              f"{np.median(lat):>7.1f} {np.percentile(lat, 90):>7.1f}")

    best_thr = max(THRESHOLDS, key=lambda t: results[f"hybrid_{t}"]["accuracy"])
    hp = results[f"hybrid_{best_thr}"]
    print(f"\nENG YAXSHI: threshold={best_thr} acc={hp['accuracy']} "
          f"fallback={hp['fallback_pct']}% med={hp['latency_median_ms']}ms")
    print("confusion matrix (eng yaxshi):")
    # recompute cm for best cfg
    preds = []
    for i in range(len(texts)):
        if sem_score[i] >= best_thr:
            preds.append(sem_pred[i])
        else:
            preds.append(lora_pred[i])
    cm = confusion_matrix(labels, np.array(preds)).tolist()
    results["best_threshold"] = best_thr
    results["confusion_matrix"] = cm
    Path("logs/inference/hybrid_router_results.json").write_text(json.dumps(results, indent=1))
    print(json.dumps(cm))
    print("Saqlendi: logs/hybrid_router_results.json")


if __name__ == "__main__":
    main()
