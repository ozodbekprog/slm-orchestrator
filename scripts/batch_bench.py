#!/usr/bin/env python3
"""Batching benchmark: llama-server --parallel bilan aggregate tok/s o'lchash.

Ishlatish (server ishlab turganida):
    .venv/bin/python scripts/batch_bench.py --port 8101
"""
from __future__ import annotations

import argparse
import asyncio
import time

import httpx

PAYLOAD = {
    "messages": [{"role": "user", "content": "Write two short sentences about the sea."}],
    "max_tokens": 64,
    "temperature": 0,
}


async def one(client: httpx.AsyncClient, url: str) -> tuple[float, int]:
    t0 = time.perf_counter()
    r = await client.post(url, json=PAYLOAD, timeout=600)
    wall = time.perf_counter() - t0
    d = r.json()
    return wall, d.get("timings", {}).get("predicted_n", 0)


async def run(url: str, n: int) -> None:
    async with httpx.AsyncClient() as client:
        t0 = time.perf_counter()
        res = await asyncio.gather(*[one(client, url) for _ in range(n)])
        wall = time.perf_counter() - t0
    toks = sum(t for _, t in res)
    per_stream = sum(t / w for w, t in res) / len(res)
    print(f"n={n:2d} | wall={wall:6.2f}s | tokens={toks:4d} | "
          f"AGGREGATE={toks/wall:7.1f} tok/s | per-stream o'rt={per_stream:6.1f} tok/s")


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8101)
    ap.add_argument("--ns", default="1,2,4,8")
    args = ap.parse_args()
    url = f"http://127.0.0.1:{args.port}/v1/chat/completions"
    print("Batching benchmark (64 token javob, bir xil savol):")
    for n in [int(x) for x in args.ns.split(",")]:
        await run(url, n)


if __name__ == "__main__":
    asyncio.run(main())
