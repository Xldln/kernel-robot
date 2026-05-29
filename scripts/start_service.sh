#!/usr/bin/env bash
# MindBridge 服务启动脚本
# 用法:
#   bash scripts/start_service.sh yolo       # 启动 YOLO (端口 8001)
#   bash scripts/start_service.sh realsense  # 启动 RealSense (端口 8000)
#   bash scripts/start_service.sh siglip     # 启动 SigLIP (端口 8002)
#   bash scripts/start_service.sh all        # 同时启动所有服务
#   bash scripts/start_service.sh stop       # 停止所有服务
#   bash scripts/start_service.sh status     # 查看运行状态
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT_DIR/logs"
PID_DIR="/tmp/mindbridge"

mkdir -p "$LOG_DIR" "$PID_DIR"

cleanup() {
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
    exit 0
}

status() {
    echo "========== Service Status =========="
    for pid_file in "$PID_DIR"/*.pid; do
        [ -f "$pid_file" ] || continue
        pid=$(cat "$pid_file")
        service=$(basename "$pid_file" .pid)
        if kill -0 "$pid" 2>/dev/null; then
            echo "  [RUNNING] $service (PID $pid)"
        else
            echo "  [DEAD] $service (stale PID $pid)"
            rm -f "$pid_file"
        fi
    done
    if ! ls "$PID_DIR"/*.pid &>/dev/null; then
        echo "  No services running"
    fi
}

start_service() {
    local name=$1
    local env_name=$2
    local script=$3
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

    echo "  [START] $name → $log_file"

    nohup bash -c "
        source \"\$(conda info --base)/etc/profile.d/conda.sh\" 2>/dev/null
        conda activate $env_name
        cd \"$ROOT_DIR\"
        exec python \"$script\"
    " > "$log_file" 2>&1 &
    local pid=$!
    echo "$pid" > "$pid_file"

    sleep 2
    if kill -0 "$pid" 2>/dev/null; then
        echo "  [OK] $name started (PID $pid)"
    else
        echo "  [FAIL] $name failed to start — check $log_file"
        rm -f "$pid_file"
        tail -5 "$log_file" 2>/dev/null || true
    fi
}

# ── Trap ──────────────────────────────────────────────────────────
trap cleanup SIGINT SIGTERM

# ── Dispatch ──────────────────────────────────────────────────────
case "${1:-help}" in
    yolo)
        start_service "yolo" "yolo" "mindbridge/src/core/launch/service_InsenceSeg.py"
        ;;
    realsense)
        start_service "realsense" "realsense" "mindbridge/src/core/launch/service_RealSense.py"
        ;;
    siglip)
        start_service "siglip" "siglip" "mindbridge/src/core/launch/service_Siglip.py"
        ;;
    all)
        start_service "realsense" "realsense" "mindbridge/src/core/launch/service_RealSense.py"
        echo ""
        start_service "yolo" "yolo" "mindbridge/src/core/launch/service_InsenceSeg.py"
        echo ""
        start_service "siglip" "siglip" "mindbridge/src/core/launch/service_Siglip.py"
        ;;
    stop)
        cleanup
        ;;
    status)
        status
        ;;
    restart)
        cleanup
        sleep 1
        start_service "realsense" "realsense" "mindbridge/src/core/launch/service_RealSense.py"
        echo ""
        start_service "yolo" "yolo" "mindbridge/src/core/launch/service_InsenceSeg.py"
        echo ""
        start_service "siglip" "siglip" "mindbridge/src/core/launch/service_Siglip.py"
        ;;
    *)
        echo "MindBridge Service Manager"
        echo ""
        echo "Usage:"
        echo "  bash $0 yolo        # YOLO 推理服务    → :8001"
        echo "  bash $0 realsense   # RealSense 深度   → :8000"
        echo "  bash $0 siglip      # SigLIP 状态分类  → :8002"
        echo "  bash $0 all         # 同时启动三个"
        echo "  bash $0 stop        # 停止所有"
        echo "  bash $0 status      # 查看状态"
        echo "  bash $0 restart     # 重启所有"
        ;;
esac
