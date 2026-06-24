#!/usr/bin/env bash
# SAM3 服务测试脚本
# 用法: bash scripts/test_sam3.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HOST="127.0.0.1"
PORT=8005
BASE_URL="http://${HOST}:${PORT}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass()  { echo -e "${GREEN}[PASS]${NC} $*"; }
fail()  { echo -e "${RED}[FAIL]${NC} $*"; }
info()  { echo -e "${YELLOW}[INFO]${NC} $*"; }

cleanup() {
    if [ -n "${SERVICE_PID:-}" ] && kill -0 "$SERVICE_PID" 2>/dev/null; then
        info "Stopping service (PID $SERVICE_PID)..."
        kill "$SERVICE_PID" 2>/dev/null || true
        wait "$SERVICE_PID" 2>/dev/null || true
    fi
    if [ -n "${TMP_IMG:-}" ]; then rm -f "$TMP_IMG"; fi
}
trap cleanup EXIT

# ── 1. 检查依赖 ──────────────────────────────────────────────────
echo "========== SAM3 Service Test =========="
echo ""

if ! python3 -c "import numpy" 2>/dev/null; then
    fail "numpy not available — run inside Docker (mindtest) or conda env"
    exit 1
fi

# ── 2. 启动服务 ──────────────────────────────────────────────────
info "Starting SAM3 service on port $PORT ..."

cd "$ROOT_DIR"
export PYTHONPATH="$ROOT_DIR${PYTHONPATH:+:$PYTHONPATH}"

python3 mindbridge/src/core/launch/service_Sam3.py &
SERVICE_PID=$!

# ── 3. 等待就绪 ──────────────────────────────────────────────────
info "Waiting for service to be ready (model loading may take 10-30s) ..."
READY=0
for i in $(seq 1 60); do
    if curl -s "$BASE_URL/health" 2>/dev/null | grep -q '"ok"'; then
        READY=1
        break
    fi
    sleep 2
    if [ $((i % 5)) -eq 0 ]; then
        echo "  ... waiting ($((i * 2))s)"
    fi
done

if [ "$READY" -eq 0 ]; then
    fail "Service did not become ready within 120s"
    exit 1
fi
pass "Service is ready"

# ── 4. Health Check ──────────────────────────────────────────────
echo ""
echo "--- Test: Health ---"
HEALTH=$(curl -s "$BASE_URL/health")
if echo "$HEALTH" | grep -q '"ok"'; then
    pass "Health endpoint: $HEALTH"
else
    fail "Health endpoint returned: $HEALTH"
fi

# ── 5. OpenAPI Docs ─────────────────────────────────────────────
echo ""
echo "--- Test: OpenAPI Docs ---"
DOCS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/docs")
if [ "$DOCS_STATUS" = "200" ]; then
    pass "Swagger UI accessible (HTTP $DOCS_STATUS)"
else
    fail "Swagger UI returned HTTP $DOCS_STATUS"
fi

# ── 6. 合成图像推理测试 ──────────────────────────────────────────
echo ""
echo "--- Test: Inference with synthetic image ---"

TMP_IMG=$(mktemp /tmp/sam3_test_XXXX.png)

python3 -c "
import cv2, numpy as np
h, w = 480, 640
np.random.seed(42)
img = (np.random.rand(h, w, 3) * 255).astype(np.uint8)
# 画一些目标
for i in range(5):
    y, x = np.random.randint(0, h-80), np.random.randint(0, w-80)
    cv2.rectangle(img, (x, y), (x+80, y+80), tuple(np.random.randint(0, 255, 3).tolist()), -1)
cv2.imwrite('$TMP_IMG', img)
print(f'Synthetic image: {w}x{h}')
"

# 写 base64 到文件，避免 shell 参数长度限制
TMP_B64=$(mktemp /tmp/sam3_b64_XXXX.txt)
base64 -w0 "$TMP_IMG" > "$TMP_B64"

TMP_JSON=$(mktemp /tmp/sam3_req_XXXX.json)
python3 -c "
import json
with open('$TMP_B64') as f:
    img_b64 = f.read().strip()
with open('$TMP_JSON', 'w') as f:
    json.dump({
        'request_id': 'synthetic_test',
        'image_b64': img_b64,
        'prompts': ['object'],
        'score_threshold': 0.3,
    }, f)
"
rm -f "$TMP_B64"

RESP=$(curl -s -X POST "$BASE_URL/infer/detect" \
  -H "Content-Type: application/json" \
  -d "@$TMP_JSON")
rm -f "$TMP_JSON"

STATUS=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('status','error'))")
ELAPSED=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('elapsed_sec',0))")
NUM_DET=$(echo "$RESP" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('detections',[])))")

if [ "$STATUS" = "ok" ]; then
    pass "Inference succeeded: elapsed=${ELAPSED}s, detections=$NUM_DET"
else
    MSG=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('message',''))" 2>/dev/null || echo "parse error")
    fail "Inference failed: $MSG"
fi

# ── 7. 错误处理测试 ─────────────────────────────────────────────
echo ""
echo "--- Test: Missing required field ---"
ERR_RESP=$(curl -s -X POST "$BASE_URL/infer/detect" \
  -H "Content-Type: application/json" \
  -d '{"request_id": "bad_req"}')
ERR_STATUS=$(echo "$ERR_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('detail',''))" 2>/dev/null || echo "parse_error")

if [ "$ERR_STATUS" != "" ]; then
    pass "Validation error correctly returned: ${ERR_STATUS:0:80}"
else
    fail "Expected validation error but got a different response"
fi

# ── 8. 总结 ──────────────────────────────────────────────────────
echo ""
echo "========== Test Complete =========="
echo "Endpoints:"
echo "  Health:  $BASE_URL/health"
echo "  Swagger: $BASE_URL/docs"
echo "  API:     POST $BASE_URL/infer/detect"
echo "            POST $BASE_URL/infer/detect/file"
