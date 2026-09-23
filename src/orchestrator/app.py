#!/usr/bin/env python3
"""SLM Orkestrator — QADAM 3: FastAPI orchestrator prototipi.

Oqim:
    POST /ask {query}
      → gibrid router (semantic CPU 5ms; score<0.5 → LoRA GPU)
      → mutaxassis llama-server (lazy start, LRU=1 — 4GB VRAM cheklovi)
      → javob qaytaradi

Mutaxassislar (port 8101-8105, -ngl 99; alloma-8B qismli offload):
    math 8101 · code 8102 · chat 8103 · image 8104 (+mmproj) · uz 8105

Ishga tushirish:
    .venv/bin/uvicorn src.orchestrator.app:app --host 127.0.0.1 --port 8200
    curl -X POST localhost:8200/ask -H 'Content-Type: application/json' -d '{"query":"Solve 3x+5=20"}'
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "router"))
from predict import RouterPredictor  # noqa: E402

LLAMA = ROOT.parent / "uz-llm-lab" / "tools" / "llama-vulkan" / "bin" / "llama-server"
MODELS = ROOT / "models"
LOGS = ROOT / "logs" / "inference"

SPECIALISTS: dict[str, dict] = {
    "math":  {"port": 8101, "args": ["-ngl", "99"]},
    "code":  {"port": 8102, "args": ["-ngl", "99"]},
    "chat":  {"port": 8103, "args": ["-ngl", "99"]},
    "image": {"port": 8104, "args": ["-ngl", "99", "--mmproj",
                                     str(MODELS / "image" / "mmproj.gguf")]},
    "uz":    {"port": 8105, "args": ["-ngl", "20", "-ot", "token_embd.weight=CPU,output.weight=CPU"]},
}

app = FastAPI(title="SLM Orkestrator", version="0.1")
state: dict = {"router": None, "procs": {}, "active": None}


class AskRequest(BaseModel):
    query: str
    max_tokens: int = 256
    temperature: float = 0.0
    route_only: bool = False


def _server_up(port: int) -> bool:
    try:
        r = httpx.get(f"http://127.0.0.1:{port}/health", timeout=2)
        return '"status":"ok"' in r.text
    except Exception:
        return False


def _wait_up(port: int, timeout: float = 120) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        if _server_up(port):
            return True
        time.sleep(1.5)
    return False


def _stop(tag: str) -> None:
    proc = state["procs"].pop(tag, None)
    if proc and proc.poll() is None:
        proc.send_signal(signal.SIGTERM)
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    if state["active"] == tag:
        state["active"] = None


def ensure_specialist(tag: str) -> bool:
    """Lazy start: VRAM 4GB → bir vaqtda bitta server."""
    if state["active"] == tag and _server_up(SPECIALISTS[tag]["port"]):
        return True
    if state["active"] is not None:
        _stop(state["active"])
    cfg = SPECIALISTS[tag]
    model = MODELS / tag / f"{tag}.gguf"
    if not model.exists():
        return False
    cmd = [str(LLAMA), "-m", str(model), "--host", "127.0.0.1",
           "--port", str(cfg["port"]), "-c", "4096", "-t", "8",
           "-fa", "auto", "--parallel", "1", *cfg["args"]]
    LOGS.mkdir(exist_ok=True)
    log = open(LOGS / f"srv_{tag}.log", "a")
    state["procs"][tag] = subprocess.Popen(cmd, stdout=log, stderr=log)
    ok = _wait_up(cfg["port"])
    if ok:
        state["active"] = tag
    else:
        _stop(tag)
    return ok


@app.on_event("startup")
def startup() -> None:
    print("Router yuklanmoqda (CPU — VRAM mutaxassislarga)...")
    state["router"] = RouterPredictor(threshold=0.5, lora_device="cpu",
                                      encoder_device="cpu")
    print("Warmup (birinchi LoRA chaqiruv sekin bo'lmasligi uchun)...")
    state["router"].predict("warmup query")
    print("Orkestrator tayyor ✅")


CHAT_HTML = """<!doctype html>
<html lang="uz">
<head>
<meta charset="utf-8">
<title>SLM Orkestrator — Chat</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { font-family: system-ui, sans-serif; max-width: 820px; margin: 0 auto; padding: 16px; background: #0f1115; color: #e8e8e8; }
  h1 { font-size: 1.15rem; margin: 0 0 10px; }
  h1 span { color: #6fa8ff; }
  #chat { border: 1px solid #2a2f3a; border-radius: 12px; padding: 12px; height: 62vh; overflow-y: auto; background: #151922; }
  .msg { margin: 8px 0; padding: 8px 12px; border-radius: 10px; white-space: pre-wrap; line-height: 1.45; }
  .user { background: #1f3a5f; margin-left: 18%; }
  .bot { background: #232833; margin-right: 18%; }
  .meta { font-size: 0.72rem; color: #9aa4b2; margin-top: 5px; }
  .row { display: flex; gap: 8px; margin-top: 10px; }
  input { flex: 1; padding: 11px; border-radius: 8px; border: 1px solid #2a2f3a; background: #151922; color: #e8e8e8; font-size: 1rem; }
  button { padding: 11px 20px; border-radius: 8px; border: 0; background: #2f6fd0; color: white; cursor: pointer; font-size: 1rem; }
  button:disabled { opacity: 0.45; cursor: wait; }
  .badge { display:inline-block; padding:1px 8px; border-radius:6px; background:#2a2f3a; font-size:0.7rem; margin-right:6px; color:#c9d4e3; }
</style>
</head>
<body>
<h1>SLM Orkestrator <span>· math · code · uz · chat · image</span></h1>
<div id="chat"></div>
<div class="row">
  <input id="q" placeholder="Savolingizni yozing (o'zbekcha ham mumkin)..." autofocus>
  <button id="send">Yuborish</button>
</div>
<script>
const chat = document.getElementById('chat');
const q = document.getElementById('q');
const btn = document.getElementById('send');
function add(cls, text, meta) {
  const d = document.createElement('div');
  d.className = 'msg ' + cls;
  d.textContent = text;
  if (meta) { const m = document.createElement('div'); m.className = 'meta'; m.textContent = meta; d.appendChild(m); }
  chat.appendChild(d); chat.scrollTop = chat.scrollHeight;
}
async function send() {
  const text = q.value.trim(); if (!text) return;
  q.value = ''; add('user', text);
  btn.disabled = true;
  const load = document.createElement('div'); load.className = 'msg bot';
  load.textContent = '...'; chat.appendChild(load); chat.scrollTop = chat.scrollHeight;
  try {
    const r = await fetch('/ask', {method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({query: text, max_tokens: 512, temperature: 0.7})});
    const d = await r.json(); load.remove();
    if (d.error) { add('bot', 'Xatolik: ' + d.error); }
    else {
      add('bot', d.answer || '(javob yo`q)',
        'route: ' + d.route + ' · ' + (d.specialist_tok_s || '?') + ' tok/s · '
        + ((d.total_ms || 0) / 1000).toFixed(1) + 's · '
        + (d.router ? d.router.source + ' (' + d.router.score + ')' : ''));
    }
  } catch (e) { load.remove(); add('bot', 'Ulanish xatosi: ' + e); }
  btn.disabled = false; q.focus();
}
btn.onclick = send;
q.addEventListener('keydown', function (e) { if (e.key === 'Enter') send(); });
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def chat_ui() -> str:
    return CHAT_HTML


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "active_specialist": state["active"],
            "loaded_router": state["router"] is not None}


@app.post("/route")
def route(req: AskRequest) -> dict:
    r = state["router"].predict(req.query)
    return r


@app.post("/ask")
def ask(req: AskRequest) -> dict:
    t0 = time.perf_counter()
    r = state["router"].predict(req.query)
    out: dict = {"route": r["route"], "router": r}
    if req.route_only:
        return out

    if not ensure_specialist(r["route"]):
        out["error"] = f"mutaxassis yuklanmadi: {r['route']}"
        out["total_ms"] = None
        return out

    port = SPECIALISTS[r["route"]]["port"]
    payload = {
        "messages": [{"role": "user", "content": req.query}],
        "max_tokens": req.max_tokens, "temperature": req.temperature,
    }
    t1 = time.perf_counter()
    try:
        resp = httpx.post(f"http://127.0.0.1:{port}/v1/chat/completions",
                          json=payload, timeout=600)
        d = resp.json()
        out["answer"] = d["choices"][0]["message"].get("content", "")
        out["specialist_tok_s"] = round(
            d.get("timings", {}).get("predicted_per_second", 0), 2)
        out["specialist_tokens"] = d.get("timings", {}).get("predicted_n", 0)
    except Exception as e:
        out["error"] = f"mutaxassis xatosi: {e}"
    out["total_ms"] = round((time.perf_counter() - t0) * 1000, 1)
    out["specialist_ms"] = round((time.perf_counter() - t1) * 1000, 1)
    return out


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1",
                port=int(os.environ.get("PORT", "8200")))
