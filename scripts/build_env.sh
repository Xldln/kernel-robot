#!/usr/bin/env bash
# MindBridge conda 环境构建脚本
# bash scripts/build_env.sh [yolo|realsense|all]
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_VER="3.12"
TORCH_CUDA="https://download.pytorch.org/whl/cu128"
MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"


set_base(){
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

    apt-get install -y fonts-dejavu-core 2>/dev/null || true
    CONDA_BASE="$(conda info --base)"
    mkdir -p "$CONDA_BASE/lib/python3.12/site-packages/cv2/qt/fonts" \
    && cp /usr/share/fonts/truetype/dejavu/*.ttf "$CONDA_BASE/lib/python3.12/site-packages/cv2/qt/fonts/"
}

_env_exists() { conda info --envs | awk '{print $1}' | grep -qx "$1"; }

build_yolo() {
    set_base
    echo "========== Building yolo env =========="
    if _env_exists yolo; then
        echo "[SKIP] yolo already exists"
    else
        conda create -n yolo python=$PYTHON_VER -y
    fi

    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate yolo

    pip config set global.index-url $MIRROR
    pip3 install torch torchvision -i $TORCH_CUDA

    if [ -d "$ROOT_DIR/models/pkg/yolo" ]; then
        cd "$ROOT_DIR/models/pkg/yolo" && pip install -e . && cd "$ROOT_DIR"
    else
        pip install ultralytics
    fi

    pip install opencv-python numpy pyyaml uvicorn fastapi pydantic python-multipart lap
    echo "========== yolo env ready =========="
}


build_lastvit() {
    set_base
    echo "========== Building lastvit env =========="
    if _env_exists lastvit; then
        echo "[SKIP] lastvit already exists"
    else
        conda create -n lastvit python=$PYTHON_VER -y
    fi

    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate lastvit
    pip config set global.index-url $MIRROR
    pip3 install torch torchvision -i $TORCH_CUDA

    pip install opencv-python numpy pyyaml uvicorn fastapi pydantic python-multipart
    echo "========== lastvit env ready =========="
}


build_realsense() {
    set_base
    echo "========== Building realsense env =========="
    apt-get update && apt-get install -y --no-install-recommends libusb-1.0-0

    if _env_exists realsense; then
        echo "[SKIP] realsense already exists"
    else
        conda create -n realsense python=$PYTHON_VER -y
    fi
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate realsense

    pip config set global.index-url $MIRROR
    pip3 install torch torchvision -i $TORCH_CUDA

    pip install pyrealsense2 omegaconf opencv-python numpy uvicorn fastapi pydantic

    echo "========== realsense env ready =========="
}

case "${1:-all}" in
    yolo)      build_yolo ;;
    lastvit)   build_lastvit ;;
    realsense) build_realsense ;;
    all)
        build_yolo
        build_lastvit
        build_realsense
        ;;
    *)
        echo "Usage: $0 [yolo|realsense|all]"
        exit 1
        ;;
esac
