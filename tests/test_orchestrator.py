#!/usr/bin/env python3
"""Orchestrator smoke testi (server ishlab turganida)."""
import httpx

BASE = "http://127.0.0.1:8200"


def _up() -> bool:
    try:
        return httpx.get(f"{BASE}/health", timeout=3).status_code == 200
    except Exception:
        return False


def test_health():
    if not _up():
        print("⚠️  Orchestrator ishlamayapti — test o'tkazib yuborildi")
        return
    d = httpx.get(f"{BASE}/health", timeout=3).json()
    assert d["status"] == "ok"
    assert d["loaded_router"] is True


def test_chat_page():
    if not _up():
        return
    r = httpx.get(f"{BASE}/", timeout=5)
    assert "SLM Orkestrator" in r.text


def test_route_endpoint():
    if not _up():
        return
    r = httpx.post(f"{BASE}/route", json={"query": "Solve 3x+5=20"}, timeout=60)
    assert r.json()["route"] == "math"


if __name__ == "__main__":
    test_health()
    test_chat_page()
    test_route_endpoint()
    print("✅ Orchestrator testlari o'tdi (yoki server o'chiq)")
