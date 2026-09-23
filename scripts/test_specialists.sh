#!/bin/bash
# QADAM 2 (qismli): tayyor mutaxassislarni llama-server sifatida alohida sinash.
# Har model: start -> health -> probe savol -> javob + tok/s -> stop.
cd "$(dirname "$0")/.." || exit 1
BIN=tools/../uz-llm-lab/tools/llama-vulkan/bin/llama-server
[ -x "$BIN" ] || BIN=../uz-llm-lab/tools/llama-vulkan/bin/llama-server
OUT=logs/specialist_tests.jsonl
: > "$OUT"

probe() {
  local tag=$1 port=$2 msg="$3"
  shift 3
  echo "[$tag] server start (port $port)..."
  "$BIN" -m "models/$tag/$tag.gguf" --host 127.0.0.1 --port "$port" \
    -ngl 99 -c 2048 -t 8 -fa auto --parallel 1 "$@" > "logs/srv_$tag.log" 2>&1 &
  local pid=$!
  local ok=0
  for i in $(seq 1 60); do
    sleep 2
    curl -sf --max-time 2 "http://127.0.0.1:$port/health" | grep -q '"status":"ok"' && { ok=1; break; }
  done
  if [ "$ok" = 1 ]; then
    curl -s --max-time 240 "http://127.0.0.1:$port/v1/chat/completions" \
      -H 'Content-Type: application/json' \
      -d "{\"messages\":[{\"role\":\"user\",\"content\":$(python3 -c "import json,sys;print(json.dumps(sys.argv[1]))" "$msg")}],\"max_tokens\":150,\"temperature\":0}" \
      | python3 -c '
import json, sys
tag = sys.argv[1]
try:
    d = json.load(sys.stdin)
    t = d.get("timings", {})
    m = d["choices"][0]["message"]
    print(json.dumps({"tag": tag, "ok": True,
                      "answer": (m.get("content") or "").strip()[:300],
                      "tok_s": round(t.get("predicted_per_second", 0), 2),
                      "tokens": t.get("predicted_n")}))
except Exception as e:
    print(json.dumps({"tag": tag, "ok": False, "error": str(e)}))
' "$tag" >> "$OUT"
  else
    echo "{\"tag\":\"$tag\",\"ok\":false,\"error\":\"server ishga tushmadi\"}" >> "$OUT"
  fi
  kill "$pid" 2>/dev/null
  wait "$pid" 2>/dev/null
  sleep 2
}

probe math 8101 "Solve 3x + 5 = 20. Show the steps briefly."
probe code 8102 "Write a Python function that returns the factorial of n."
probe chat 8103 "Say hello in one sentence and tell me one fun fact."
echo "=== natijalar ==="
cat "$OUT"
