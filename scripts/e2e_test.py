#!/usr/bin/env python3
"""SLM Orkestrator — end-to-end test (orchestrator ishlab turganida).

QADAM 1: 3 ta tez test (math, code, chat) — jadval.
QADAM 2: 20 savol benchmark — routing aniqlik, latency, throughput, xato tahlili.

Ishlatish:
    .venv/bin/python scripts/e2e_test.py
"""
from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "router"))
from predict import TEST_QUESTIONS  # noqa: E402

BASE = "http://127.0.0.1:8200"
OUT = ROOT / "logs" / "inference" / "e2e_results.json"

QUICK = [
    ("Solve 3x + 5 = 20. Answer briefly.", "math"),
    ("Write a Python one-liner to reverse a string.", "code"),
    ("Say hello and tell one fun fact.", "chat"),
]


def wait_up(timeout: float = 180) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = httpx.get(f"{BASE}/health", timeout=3)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(2)
    return False


def ask(query: str, max_tokens: int = 64) -> dict:
    t0 = time.perf_counter()
    r = httpx.post(f"{BASE}/ask", json={"query": query, "max_tokens": max_tokens,
                                        "temperature": 0.0}, timeout=900)
    wall = (time.perf_counter() - t0) * 1000
    d = r.json()
    d["wall_ms"] = round(wall, 1)
    return d


def main() -> None:
    if not wait_up():
        print("Orchestrator ishga tushmadi!")
        sys.exit(1)
    print("Orchestrator tayyor ✅\n")

    print("=" * 100)
    print("QADAM 1: 3 ta tez test")
    print("=" * 100)
    quick_rows = []
    for q, expected in QUICK:
        d = ask(q, max_tokens=80)
        row = {"query": q, "expected": expected, "route": d.get("route"),
               "ok": d.get("route") == expected,
               "router_ms": d.get("router", {}).get("latency_ms"),
               "total_ms": d.get("total_ms"), "wall_ms": d.get("wall_ms"),
               "tok_s": d.get("specialist_tok_s"),
               "answer": (d.get("answer") or d.get("error") or "")[:110]}
        quick_rows.append(row)
        print(f"\n[{d.get('route'):5s}] ({'✅' if row['ok'] else '❌'}) "
              f"router={row['router_ms']}ms total={row['total_ms']}ms tok/s={row['tok_s']}")
        print(f"  savol : {q}")
        print(f"  javob : {row['answer']}")

    print("\n" + "=" * 100)
    print("QADAM 2: 20 savol benchmark")
    print("=" * 100)
    print(f"{'#':>2s} {'kutilgan':>8s} {'route':>8s} {'manba':>8s} {'r_ms':>6s} "
          f"{'e2e_ms':>8s} {'tok/s':>6s} {'OK':>3s}  savol")
    print("-" * 110)
    results = []
    for i, (q, expected) in enumerate(TEST_QUESTIONS, 1):
        d = ask(q, max_tokens=64)
        served = d.get("total_ms") is not None
        row = {"query": q, "expected": expected, "route": d.get("route"),
               "source": d.get("router", {}).get("source"),
               "score": d.get("router", {}).get("score"),
               "router_ms": d.get("router", {}).get("latency_ms"),
               "total_ms": d.get("total_ms"), "wall_ms": d.get("wall_ms"),
               "tok_s": d.get("specialist_tok_s"),
               "tokens": d.get("specialist_tokens", 0),
               "served": served, "error": d.get("error"),
               "ok": d.get("route") == expected,
               "answer": (d.get("answer") or "")[:80]}
        results.append(row)
        t_str = f"{row['total_ms']:.0f}" if served else "  —"
        tok_str = f"{row['tok_s']:.0f}" if row["tok_s"] else "  —"
        print(f"{i:>2d} {expected:>8s} {str(row['route']):>8s} {str(row['source']):>8s} "
              f"{row['router_ms']:>6.1f} {t_str:>8s} "
              f"{tok_str:>6s} {'✅' if row['ok'] else '❌'}"
              f"{' ⏭' if not served else '  '} {q[:40]}")

    n = len(results)
    n_ok = sum(r["ok"] for r in results)
    served = [r for r in results if r["served"]]
    r_ms = [r["router_ms"] for r in results if r["router_ms"]]
    t_ms = [r["total_ms"] for r in served]
    tok = [r["tok_s"] for r in served if r["tok_s"]]
    total_tokens = sum(r["tokens"] for r in served)
    total_wall = sum(r["wall_ms"] for r in served)
    acc = 100 * n_ok / n
    print("-" * 110)
    print(f"Routing aniqlik : {n_ok}/{n} = {acc:.1f}%")
    print(f"Router latency  : med {statistics.median(r_ms):.1f} ms | p90 {sorted(r_ms)[int(0.9*len(r_ms))-1]:.1f} ms")
    if t_ms:
        print(f"E2E latency     : med {statistics.median(t_ms):.0f} ms | maks {max(t_ms):.0f} ms "
              f"({len(served)}/{n} savol xizmat ko'rsatildi)")
    if tok:
        print(f"Mutaxassis tezlik: med {statistics.median(tok):.1f} tok/s")
    if total_wall:
        print(f"Throughput      : {total_tokens} token / {total_wall/1000:.1f}s = "
              f"{total_tokens/(total_wall/1000):.1f} tok/s (wall)")
    unavail = [r for r in results if not r["served"]]
    if unavail:
        print(f"⏭ Model kutilmoqda ({len(unavail)}): " +
              ", ".join(sorted({r['route'] for r in unavail})))

    errs = [r for r in results if not r["ok"]]
    if errs:
        print("\nXatolar tahlili:")
        for r in errs:
            print(f"  ❌ '{r['query'][:50]}' kutilgan={r['expected']} "
                  f"topildi={r['route']} (score={r['score']}, {r['source']})")

    OUT.write_text(json.dumps({
        "quick": quick_rows, "benchmark": results,
        "routing_accuracy": acc,
        "router_latency_median_ms": statistics.median(r_ms),
        "e2e_latency_median_ms": statistics.median(t_ms),
        "total_tokens": total_tokens,
        "wall_seconds": round(total_wall / 1000, 1),
    }, indent=1, ensure_ascii=False))
    print(f"\nSaqlendi: {OUT}")


if __name__ == "__main__":
    main()
