#!/usr/bin/env bash
# MindBridge 服务启动脚本
# 用法:
#   bash scripts/start_service.sh yolo            # 启动 YOLO (端口 8001)
#   bash scripts/start_service.sh realsense       # 启动 RealSense (端口 8000)
#   bash scripts/start_service.sh siglip          # 启动 SigLIP (端口 8002)
#   bash scripts/start_service.sh fastfoundation  # 启动 FastFoundation (端口 8004)
#   bash scripts/start_service.sh sam3            # 启动 SAM3 (端口 8005)
#   bash scripts/start_service.sh flowpose        # 启动 FlowPose (端口 8006)
#   bash scripts/start_service.sh yolo-full       # 并行启动 YOLO full 依赖
#   bash scripts/start_service.sh sam3-full       # 并行启动 SAM3 full 依赖
#   bash scripts/start_service.sh all             # 并行启动所有服务
#   bash scripts/start_service.sh stop            # 停止所有服务
#   bash scripts/start_service.sh status          # 查看运行状态
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT_DIR/logs"
PID_DIR="/tmp/mindbridge"

mkdir -p "$LOG_DIR" "$PID_DIR"

stop_services() {
    echo ""
    echo "Stopping all services..."
    for pid_file in "$PID_DIR"/*.pid; do
        [ -f "$pid_file" ] || continue
        pid=$(cat "$pid_file")
        service=$(basename "$pid_file" .pid)
        if kill "$pid" 2>/dev/null; then
            echo "  [STOPPED] $service (PID $pid)"
        else
            echo "  [NOT RUNNING] $service"
        fi
        rm -f "$pid_file"
    done
}

cleanup() {
    stop_services
    exit 0
}

port_open() {
    local port=$1
    timeout 1 bash -c ":</dev/tcp/127.0.0.1/$port" &>/dev/null
}

http_ok() {
    local url=$1
    if command -v curl >/dev/null 2>&1; then
        curl -fsS --max-time 1 "$url" >/dev/null 2>&1
        return
    fi
    python - "$url" <<'PY' >/dev/null 2>&1
import sys
from urllib.request import urlopen
urlopen(sys.argv[1], timeout=1).read()
PY
}

service_ready_on_port() {
    local name=$1
    local port=$2

    if [ "$name" = "realsense" ]; then
        http_ok "http://127.0.0.1:$port/realsense/info"
        return
    fi

    http_ok "http://127.0.0.1:$port/health"
}

pid_for_port() {
    local port=$1

    if command -v ss >/dev/null 2>&1; then
        ss -ltnp "sport = :$port" 2>/dev/null \
            | sed -n 's/.*pid=\([0-9]\+\).*/\1/p' \
            | head -1
        return 0
    fi

    if command -v lsof >/dev/null 2>&1; then
        lsof -nP -iTCP:"$port" -sTCP:LISTEN -t 2>/dev/null | head -1
        return 0
    fi

    if command -v fuser >/dev/null 2>&1; then
        fuser "$port"/tcp 2>/dev/null | awk '{print $1}'
        return 0
    fi
}

status() {
    echo "========== Service Status =========="
    local found=0

    for pid_file in "$PID_DIR"/*.pid; do
        [ -f "$pid_file" ] || continue
        found=1
        pid=$(cat "$pid_file")
        service=$(basename "$pid_file" .pid)
        if kill -0 "$pid" 2>/dev/null; then
            echo "  [RUNNING] $service (PID $pid)"
        else
            echo "  [DEAD] $service (stale PID $pid)"
            rm -f "$pid_file"
        fi
    done

    for spec in \
        "realsense:8000" \
        "yolo:8001" \
        "siglip:8002" \
        "fastfoundation:8004" \
        "sam3:8005" \
        "flowpose:8006"; do
        local service="${spec%%:*}"
        local port="${spec##*:}"
        local pid_file="$PID_DIR/$service.pid"
        [ -f "$pid_file" ] && continue
        if port_open "$port"; then
            found=1
            local pid
            pid=$(pid_for_port "$port" || true)
            if [ -n "$pid" ]; then
                echo "  [RUNNING] $service port :$port (PID $pid, missing pid file)"
            else
                echo "  [RUNNING] $service port :$port (missing pid file)"
            fi
        fi
    done

    if [ "$found" -eq 0 ]; then
        echo "  No services running"
    fi
}

start_service() {
    local name=$1
    local env_name=$2
    local script=$3
    local port=$4
    local pid_file="$PID_DIR/$name.pid"
    local log_file="$LOG_DIR/${name}.log"

    if [ -f "$pid_file" ]; then
        local old_pid
        old_pid=$(cat "$pid_file")
        if kill -0 "$old_pid" 2>/dev/null; then
            echo "  [SKIP] $name already running (PID $old_pid)"
            return
        fi
        echo "  [CLEAN] $name stale PID removed"
        rm -f "$pid_file"
    fi

    if port_open "$port"; then
        if ! service_ready_on_port "$name" "$port"; then
            echo "  [WARN] $name port :$port is open but service is not ready"
            echo "  [WARN] stop the stale listener on :$port, then start $name again"
            return 1
        fi
        local port_pid
        port_pid=$(pid_for_port "$port" || true)
        if [ -n "$port_pid" ]; then
            echo "$port_pid" > "$pid_file"
            echo "  [SKIP] $name already listening on :$port (PID $port_pid)"
        else
            echo "  [SKIP] $name already listening on :$port"
        fi
        return
    fi

    echo "  [START] $name -> $log_file"

    nohup bash -c "
        source \"\$(conda info --base)/etc/profile.d/conda.sh\" 2>/dev/null
        conda activate $env_name
        cd \"$ROOT_DIR\"
        export PYTHONPATH=\"\$ROOT_DIR:\$PYTHONPATH\"
        exec python \"$script\"
    " > "$log_file" 2>&1 &
    local pid=$!
    echo "$pid" > "$pid_file"

    sleep 0.3
    if kill -0 "$pid" 2>/dev/null; then
        echo "  [OK] $name started (PID $pid)"
    else
        echo "  [FAIL] $name failed to start - check $log_file"
        rm -f "$pid_file"
        tail -5 "$log_file" 2>/dev/null || true
        return 1
    fi
}

start_named_service() {
    case "$1" in
        yolo)
            start_service "yolo" "yolo" "mindbridge/src/core/launch/service_InsenceSeg.py" 8001
            ;;
        realsense)
            start_service "realsense" "realsense" "mindbridge/src/core/launch/service_RealSense.py" 8000
            ;;
        siglip)
            start_service "siglip" "siglip" "mindbridge/src/core/launch/service_Siglip.py" 8002
            ;;
        fastfoundation)
            start_service "fastfoundation" "fastfoundation" "mindbridge/src/core/launch/service_FastFoundation.py" 8004
            ;;
        sam3)
            start_service "sam3" "sam3" "mindbridge/src/core/launch/service_Sam3.py" 8005
            ;;
        flowpose)
            start_service "flowpose" "flowpose" "mindbridge/src/core/launch/service_FlowPose.py" 8006
            ;;
        *)
            echo "Unknown service: $1" >&2
            return 2
            ;;
    esac
}

start_services_parallel() {
    local pids=()
    local service

    for service in "$@"; do
        (start_named_service "$service") &
        pids+=("$!")
    done

    local rc=0
    local pid
    for pid in "${pids[@]}"; do
        wait "$pid" || rc=1
    done
    return "$rc"
}

# ── Trap ──────────────────────────────────────────────────────────
trap cleanup SIGINT SIGTERM

# ── Dispatch ──────────────────────────────────────────────────────
case "${1:-help}" in
    yolo|realsense|siglip|fastfoundation|sam3|flowpose)
        start_named_service "$1"
        ;;
    yolo-full)
        start_services_parallel realsense fastfoundation yolo flowpose siglip
        ;;
    sam3-full)
        start_services_parallel realsense fastfoundation sam3 flowpose siglip
        ;;
    basic-yolo)
        start_services_parallel realsense yolo siglip
        ;;
    basic-sam3)
        start_services_parallel realsense sam3 siglip
        ;;
    flowpose-stack)
        start_services_parallel realsense fastfoundation flowpose
        ;;
    all)
        start_services_parallel realsense yolo siglip fastfoundation sam3 flowpose
        ;;
    stop)
        cleanup
        ;;
    status)
        status
        ;;
    restart)
        stop_services
        sleep 1
        start_services_parallel realsense yolo siglip fastfoundation sam3 flowpose
        ;;
    *)
        echo "MindBridge Service Manager"
        echo ""
        echo "Usage:"
        echo "  bash $0 yolo            # YOLO 推理服务          -> :8001"
        echo "  bash $0 realsense       # RealSense 深度         -> :8000"
        echo "  bash $0 siglip          # SigLIP 状态分类        -> :8002"
        echo "  bash $0 fastfoundation  # FastFoundation 立体    -> :8004"
        echo "  bash $0 sam3            # SAM3 检测/分割         -> :8005"
        echo "  bash $0 flowpose        # FlowPose 6D 姿态       -> :8006"
        echo "  bash $0 yolo-full       # 并行启动 YOLO full 依赖"
        echo "  bash $0 sam3-full       # 并行启动 SAM3 full 依赖"
        echo "  bash $0 basic-yolo      # 并行启动 YOLO basic 依赖"
        echo "  bash $0 basic-sam3      # 并行启动 SAM3 basic 依赖"
        echo "  bash $0 all             # 并行启动所有"
        echo "  bash $0 stop            # 停止所有"
        echo "  bash $0 status          # 查看状态"
        echo "  bash $0 restart         # 重启所有"
        ;;
esac
