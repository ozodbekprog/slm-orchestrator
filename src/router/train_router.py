#!/usr/bin/env python3
"""SLM Orkestrator — BOSQICH 3/4: router o'qitish (Qwen2.5-0.5B + LoRA).

- 5 sinf: math | code | uz | chat | image
- LoRA r=16, alpha=32, target: attention + MLP; classifier head ham o'qitiladi
- fp32 (bu GPU'da fp16 5x sekin), batch=2, grad_accum=16 (effektiv 32)
- Eval: accuracy, per-class F1, confusion matrix, latency (ms/query)

Ishlatish:
    .venv/bin/python router/train_router.py
    .venv/bin/python router/train_router.py --epochs 3 --max-len 64
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from datasets import load_dataset
from peft import LoraConfig, TaskType, get_peft_model
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

CLASSES = ["math", "code", "uz", "chat", "image"]
BASE_MODEL = "models/qwen2.5-0.5b-instruct"
OUT_DIR = Path("models/router/checkpoints")
LOG_DIR = Path("logs/training")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--epochs", type=float, default=3.0)
    ap.add_argument("--max-len", type=int, default=64)
    ap.add_argument("--batch", type=int, default=2)
    ap.add_argument("--grad-accum", type=int, default=16)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--lora-r", type=int, default=16)
    ap.add_argument("--lora-alpha", type=int, default=32)
    ap.add_argument("--max-steps", type=int, default=-1, help="test uchun kichik qiymat")
    return ap.parse_args()


def compute_metrics(eval_pred) -> dict:
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": float(accuracy_score(labels, preds)),
        "f1_macro": float(f1_score(labels, preds, average="macro")),
        "f1_weighted": float(f1_score(labels, preds, average="weighted")),
    }


def main() -> None:
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    dev = "cuda" if torch.cuda.is_available() else "cpu"

    print("=== Ma'lumotlar ===")
    ds = load_dataset("json", data_files={
        "train": "data/router_train.jsonl", "eval": "data/router_eval.jsonl"})
    print(f"train: {len(ds['train'])}, eval: {len(ds['eval'])}")

    print("=== Model + LoRA ===")
    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL, num_labels=len(CLASSES), torch_dtype=torch.float32)
    model.config.pad_token_id = tok.pad_token_id

    lora = LoraConfig(
        task_type=TaskType.SEQ_CLS,
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        modules_to_save=["score"],
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    def tokenize(batch):
        enc = tok(batch["text"], truncation=True, max_length=args.max_len)
        enc["labels"] = batch["label_id"]
        return enc

    ds = ds.map(tokenize, batched=True, remove_columns=["text", "label"])
    collator = DataCollatorWithPadding(tok)

    targs = TrainingArguments(
        output_dir=str(OUT_DIR),
        per_device_train_batch_size=args.batch,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        num_train_epochs=args.epochs,
        max_steps=args.max_steps,
        warmup_steps=50,
        logging_steps=25,
        eval_strategy="steps",
        eval_steps=200,
        save_strategy="no",
        report_to=[],
        fp16=False,
        bf16=False,
        dataloader_num_workers=2,
        optim="adamw_torch",
        seed=42,
    )

    trainer = Trainer(
        model=model, args=targs,
        train_dataset=ds["train"], eval_dataset=ds["eval"],
        data_collator=collator, compute_metrics=compute_metrics,
        processing_class=tok,
    )
    print("=== O'qitish boshlandi ===")
    t0 = time.time()
    trainer.train()
    train_min = (time.time() - t0) / 60
    print(f"O'qitish tugadi: {train_min:.1f} daqiqa")

    print("=== Yakuniy eval ===")
    metrics = trainer.evaluate()
    pred_out = trainer.predict(ds["eval"])
    preds = np.argmax(pred_out.predictions, axis=-1)
    labels = pred_out.label_ids
    cm = confusion_matrix(labels, preds).tolist()
    f1_per = f1_score(labels, preds, average=None).tolist()

    print("=== Latency benchmark (GPU, 100 query) ===")
    model.eval()
    texts = [ds["eval"][i]["input_ids"] for i in range(min(100, len(ds["eval"])))]
    lat = []
    with torch.no_grad():
        for ids in texts:
            input_ids = torch.tensor([ids], device=dev)
            mask = torch.ones_like(input_ids)
            if dev == "cuda":
                torch.cuda.synchronize()
            t = time.perf_counter()
            model(input_ids=input_ids, attention_mask=mask)
            if dev == "cuda":
                torch.cuda.synchronize()
            lat.append((time.perf_counter() - t) * 1000)
    lat_ms = float(np.median(lat))

    model.save_pretrained("models/router/lora_adapter")
    tok.save_pretrained("models/router/lora_adapter")
    results = {
        "train_minutes": round(train_min, 1),
        "accuracy": round(metrics["eval_accuracy"], 4),
        "f1_macro": round(metrics["eval_f1_macro"], 4),
        "f1_weighted": round(metrics["eval_f1_weighted"], 4),
        "f1_per_class": {c: round(v, 4) for c, v in zip(CLASSES, f1_per)},
        "confusion_matrix": cm,
        "latency_ms_gpu": round(lat_ms, 2),
    }
    (LOG_DIR / "router_results.json").write_text(json.dumps(results, indent=1))
    print(json.dumps({k: v for k, v in results.items() if k != "confusion_matrix"}, indent=1))
    print(f"Adapter saqlandi: router/lora_adapter")


if __name__ == "__main__":
    main()
