#!/usr/bin/env bash
# FastFoundation Stereo 服务测试脚本
# 用法: bash scripts/test_fastfoundation.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HOST="127.0.0.1"
PORT=8004
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
    if [ -n "${TMP_LEFT:-}" ]; then rm -f "$TMP_LEFT"; fi
    if [ -n "${TMP_RIGHT:-}" ]; then rm -f "$TMP_RIGHT"; fi
}
trap cleanup EXIT

# ── 1. 检查依赖 ──────────────────────────────────────────────────
echo "========== FastFoundation Service Test =========="
echo ""

if ! python3 -c "import numpy" 2>/dev/null; then
    fail "numpy not available — run inside Docker (mindtest) or conda env"
    exit 1
fi

# ── 2. 启动服务 ──────────────────────────────────────────────────
info "Starting FastFoundation service on port $PORT ..."

cd "$ROOT_DIR"
export PYTHONPATH="$ROOT_DIR${PYTHONPATH:+:$PYTHONPATH}"

python3 mindbridge/src/core/launch/service_FastFoundation.py &
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

# ── 6. 合成双目图像推理测试 ──────────────────────────────────────
echo ""
echo "--- Test: Inference with synthetic stereo pair ---"

TMP_LEFT=$(mktemp /tmp/ff_left_XXXX.png)
TMP_RIGHT=$(mktemp /tmp/ff_right_XXXX.png)

python3 -c "
import cv2, numpy as np

# 生成合成立体对：随机纹理 + 水平视差
h, w = 256, 320
# 左图：随机纹理
np.random.seed(42)
img = (np.random.rand(h, w, 3) * 255).astype(np.uint8)
# 加入一些结构化图案方便匹配
for i in range(20):
    y, x = np.random.randint(0, h-30), np.random.randint(0, w-30)
    cv2.rectangle(img, (x, y), (x+30, y+30), tuple(np.random.randint(0, 255, 3).tolist()), -1)

cv2.imwrite('$TMP_LEFT', img)

# 右图：左图 + 水平偏移模拟视差
shift = 16
M = np.float32([[1, 0, -shift], [0, 1, 0]])
right = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
cv2.imwrite('$TMP_RIGHT', right)

print(f'Synthetic stereo pair: {w}x{h}, shift={shift}px')
"

# 写 base64 到文件，避免 shell 参数长度限制
TMP_LEFT_B64=$(mktemp /tmp/ff_left_b64_XXXX.txt)
TMP_RIGHT_B64=$(mktemp /tmp/ff_right_b64_XXXX.txt)
base64 -w0 "$TMP_LEFT" > "$TMP_LEFT_B64"
base64 -w0 "$TMP_RIGHT" > "$TMP_RIGHT_B64"

TMP_JSON=$(mktemp /tmp/ff_req_XXXX.json)
python3 -c "
import json
with open('$TMP_LEFT_B64') as f: left_b64 = f.read().strip()
with open('$TMP_RIGHT_B64') as f: right_b64 = f.read().strip()
with open('$TMP_JSON', 'w') as f:
    json.dump({
        'request_id': 'synthetic_test',
        'left_image_b64': left_b64,
        'right_image_b64': right_b64,
        'return_depth': True,
        'return_disparity': True,
    }, f)
"
rm -f "$TMP_LEFT_B64" "$TMP_RIGHT_B64"

RESP=$(curl -s -X POST "$BASE_URL/infer/stereo" \
  -H "Content-Type: application/json" \
  -d "@$TMP_JSON")
rm -f "$TMP_JSON"

STATUS=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('status','error'))")
ELAPSED=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('elapsed_sec',0))")
DEPTH_SHAPE=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('depth_shape',[]))")
HAS_DEPTH=$(echo "$RESP" | python3 -c "import json,sys; d=json.load(sys.stdin).get('depth_u16_b64',''); print('yes' if d else 'no')")
HAS_DISP=$(echo "$RESP" | python3 -c "import json,sys; d=json.load(sys.stdin).get('disparity_b64',''); print('yes' if d else 'no')")

if [ "$STATUS" = "ok" ]; then
    pass "Inference succeeded: elapsed=${ELAPSED}s, depth_shape=$DEPTH_SHAPE, depth=$HAS_DEPTH, disp=$HAS_DISP"
else
    MSG=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('message',''))" 2>/dev/null || echo "parse error")
    fail "Inference failed: $MSG"
fi

# ── 7. 错误处理测试 ─────────────────────────────────────────────
echo ""
echo "--- Test: Missing required field ---"
ERR_RESP=$(curl -s -X POST "$BASE_URL/infer/stereo" \
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
echo "  API:     POST $BASE_URL/infer/stereo"
echo "            POST $BASE_URL/infer/stereo/file"
