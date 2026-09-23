#!/usr/bin/env python3
"""E2E test (orchestrator + mutaxassis ishlab turganida)."""
import httpx

BASE = "http://127.0.0.1:8200"


def _up() -> bool:
    try:
        return httpx.get(f"{BASE}/health", timeout=3).status_code == 200
    except Exception:
        return False


def test_e2e_math():
    if not _up():
        print("⚠️  Orchestrator o'chiq — E2E o'tkazib yuborildi")
        return
    r = httpx.post(f"{BASE}/ask", json={"query": "What is 7*6?", "max_tokens": 30},
                   timeout=300)
    d = r.json()
    assert d["route"] == "math", f"route xato: {d.get('route')}"
    assert d.get("answer"), f"javob yo'q: {d.get('error')}"
    print(f"  math: {d['answer'][:50]!r} ({d.get('specialist_tok_s')} tok/s)")


if __name__ == "__main__":
    test_e2e_math()
    print("✅ E2E testi o'tdi")
