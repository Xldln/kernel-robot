#!/usr/bin/env bash
# FlowPose 6D姿态估计服务测试脚本
# 用法: bash scripts/test_flowpose.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HOST="127.0.0.1"
PORT=8006
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
}
trap cleanup EXIT

# ── 1. 检查依赖 ──────────────────────────────────────────────────
echo "========== FlowPose Service Test =========="
echo ""

if ! python3 -c "import numpy" 2>/dev/null; then
    fail "numpy not available — run inside Docker (mindtest) or conda env"
    exit 1
fi

# ── 2. 启动服务 ──────────────────────────────────────────────────
info "Starting FlowPose service on port $PORT ..."

cd "$ROOT_DIR"
export PYTHONPATH="$ROOT_DIR${PYTHONPATH:+:$PYTHONPATH}"

python3 mindbridge/src/core/launch/service_FlowPose.py &
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

# ── 6. 错误处理测试 ─────────────────────────────────────────────
echo ""
echo "--- Test: Missing required field ---"
ERR_RESP=$(curl -s -X POST "$BASE_URL/infer/pose" \
  -H "Content-Type: application/json" \
  -d '{"request_id": "bad_req"}')
ERR_DETAIL=$(echo "$ERR_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('detail',''))" 2>/dev/null || echo "parse_error")

if [ "$ERR_DETAIL" != "" ]; then
    pass "Validation error correctly returned: ${ERR_DETAIL:0:80}"
else
    fail "Expected validation error but got a different response"
fi

# ── 7. 总结 ──────────────────────────────────────────────────────
echo ""
echo "========== Test Complete =========="
echo "Endpoints:"
echo "  Health:  $BASE_URL/health"
echo "  Swagger: $BASE_URL/docs"
echo "  API:     POST $BASE_URL/infer/pose"
echo "            POST $BASE_URL/infer/pose/file"
