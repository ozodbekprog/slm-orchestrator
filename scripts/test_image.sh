#!/bin/bash
# QADAM 3a: image mutaxassis (Qwen2-VL-2B + mmproj) testi — sintetik rasm bilan.
cd "$(dirname "$0")/.." || exit 1
BIN=../uz-llm-lab/tools/llama-vulkan/bin/llama-server
PORT=8104

.venv/bin/python - <<'EOF'
from PIL import Image, ImageDraw
img = Image.new("RGB", (640, 480), "white")
d = ImageDraw.Draw(img)
d.rectangle([50, 50, 300, 250], fill="blue")
d.ellipse([350, 50, 600, 250], fill="red")
d.text((60, 300), "HELLO KRONOS 42", fill="black")
img.save("tests/fixtures/vision_test.png")
print("test rasm: tests/fixtures/vision_test.png")
EOF

"$BIN" -m models/image/image.gguf --mmproj models/image/mmproj.gguf \
  --host 127.0.0.1 --port $PORT -ngl 99 -c 4096 -t 8 --parallel 1 \
  > logs/srv_image_test.log 2>&1 &
PID=$!
trap 'kill $PID 2>/dev/null' EXIT

ok=0
for i in $(seq 1 90); do
  sleep 2
  curl -sf --max-time 2 "http://127.0.0.1:$PORT/health" | grep -q '"status":"ok"' && { ok=1; break; }
done
if [ "$ok" != 1 ]; then
  echo "server ishga tushmadi"; tail -5 logs/srv_image_test.log; exit 1
fi

IMG_B64=$(base64 -w0 tests/fixtures/vision_test.png)
echo "rasm yuborilmoqda ($(stat -c%s tests/fixtures/vision_test.png) bayt)..."
curl -s --max-time 300 "http://127.0.0.1:$PORT/v1/chat/completions" \
  -H 'Content-Type: application/json' \
  -d "{\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"What do you see in this image? Describe colors, shapes and any text. One or two sentences.\"},{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/png;base64,$IMG_B64\"}}]}],\"max_tokens\":120,\"temperature\":0}" \
  | python3 -c '
import json, sys
d = json.load(sys.stdin)
t = d.get("timings", {})
m = d["choices"][0]["message"]
print("JAVOB :", (m.get("content") or "").strip()[:250])
print("tok/s :", round(t.get("predicted_per_second", 0), 2))
print("tokens:", t.get("predicted_n"))
'
kill $PID 2>/dev/null
echo "image server to'xtatildi"
