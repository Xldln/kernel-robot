#!/usr/bin/env bash
# MindBridge conda 环境构建脚本
# bash scripts/build_env.sh [yolo|siglip|realsense|all]
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

    chmod +x "$ROOT_DIR/bin/mind"
    for _d in /usr/local/bin "$HOME/.local/bin" "$HOME/bin"; do
        if echo ":$PATH:" | grep -q ":$_d:"; then
            mkdir -p "$_d"
            if ! ln -sf "$ROOT_DIR/bin/mind" "$_d/mind" 2>/dev/null; then
                echo "[SKIP] mind already exists at $_d/mind or same file"
            else
                echo "[INFO] mind command installed -> $_d/mind"
            fi
            break
        fi
    done

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


build_siglip() {
    set_base
    echo "========== Building siglip env =========="
    if _env_exists siglip; then
        echo "[SKIP] siglip already exists"
    else
        conda create -n siglip python=$PYTHON_VER -y
    fi

    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate siglip
    pip config set global.index-url $MIRROR
    pip3 install torch torchvision -i $TORCH_CUDA

    pip install opencv-python numpy pyyaml uvicorn fastapi pydantic python-multipart transformers
    echo "========== siglip env ready =========="
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
    siglip)    build_siglip ;;
    realsense) build_realsense ;;
    all)
        build_yolo
        build_siglip
        build_realsense
        ;;
    *)
        echo "Usage: $0 [yolo|siglip|realsense|all]"
        exit 1
        ;;
esac
