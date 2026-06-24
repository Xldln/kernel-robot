#!/usr/bin/env bash
# MindBridge conda 环境构建脚本
# bash scripts/build_env.sh [yolo|siglip|realsense|fastfoundation|sam3|all]
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_VER="3.12"
TORCH_CUDA="https://download.pytorch.org/whl/cu128"
TORCH_CUDA_FALLBACK="https://mirrors.aliyun.com/pytorch-wheels/cu128"
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

_install_torch() {
    # 安装 PyTorch CUDA 版本，主源失败自动回退备用源
    pip3 install torch torchvision -i "$TORCH_CUDA" --extra-index-url "$MIRROR" || {
        echo "[WARN] 主源 ($TORCH_CUDA) 不可达，尝试备用源 ($TORCH_CUDA_FALLBACK) ..."
        pip3 install torch torchvision -i "$TORCH_CUDA_FALLBACK" --extra-index-url "$MIRROR"
    }
}

build_yolo() {
    if _env_exists yolo; then
        echo "[SKIP] yolo already exists"
        return 0
    fi
    set_base
    echo "========== Building yolo env =========="
    conda create -n yolo python=$PYTHON_VER -y

    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate yolo

    pip config set global.index-url $MIRROR
    _install_torch

    if [ -d "$ROOT_DIR/mindbridge/models/pkg/yolo" ]; then
        cd "$ROOT_DIR/mindbridge/models/pkg/yolo" && pip install -e . && cd "$ROOT_DIR"
    else
        pip install ultralytics
    fi

    pip install opencv-python numpy pyyaml uvicorn fastapi pydantic python-multipart lap
    echo "========== yolo env ready =========="
}


build_siglip() {
    if _env_exists siglip; then
        echo "[SKIP] siglip already exists"
        return 0
    fi
    set_base
    echo "========== Building siglip env =========="
    conda create -n siglip python=$PYTHON_VER -y

    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate siglip
    pip config set global.index-url $MIRROR
    _install_torch

    pip install opencv-python numpy pyyaml uvicorn fastapi pydantic python-multipart transformers
    echo "========== siglip env ready =========="
}


build_realsense() {
    if _env_exists realsense; then
        echo "[SKIP] realsense already exists"
        return 0
    fi
    set_base
    echo "========== Building realsense env =========="
    apt-get update && apt-get install -y --no-install-recommends libusb-1.0-0

    conda create -n realsense python=$PYTHON_VER -y
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate realsense

    pip config set global.index-url $MIRROR
    _install_torch

    pip install pyrealsense2 omegaconf opencv-python numpy uvicorn fastapi pydantic

    echo "========== realsense env ready =========="
}


build_fastfoundation() {
    if _env_exists fastfoundation; then
        echo "[SKIP] fastfoundation already exists"
        return 0
    fi
    set_base
    echo "========== Building fastfoundation env =========="
    conda create -n fastfoundation python=$PYTHON_VER -y
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate fastfoundation

    pip config set global.index-url $MIRROR
    _install_torch

    # FastFoundation 核心依赖 (requirements.txt: timm, einops, scipy, scikit-image, open3d, imageio)
    pip install timm einops scipy scikit-image open3d imageio

    # 服务相关依赖 (opencv-contrib-python 覆盖 opencv-python)
    pip install omegaconf opencv-contrib-python numpy pyyaml uvicorn fastapi pydantic python-multipart

    echo "========== fastfoundation env ready =========="
}


build_sam3() {
    if _env_exists sam3; then
        echo "[SKIP] sam3 already exists"
        return 0
    fi
    set_base
    echo "========== Building sam3 env =========="
    conda create -n sam3 python=$PYTHON_VER -y
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate sam3

    pip config set global.index-url $MIRROR
    _install_torch

    # 先装服务依赖（之后 SAM3 安装时会约束 numpy<2）
    pip install opencv-python "numpy<2" pyyaml uvicorn fastapi pydantic python-multipart pillow matplotlib

    # SAM3 核心依赖 (pyproject.toml + 所有隐式依赖: scipy, pandas, scikit-learn, torchmetrics, triton)
    pip install timm ftfy regex iopath huggingface_hub transformers einops decord pycocotools psutil scipy pandas scikit-learn torchmetrics

    # 安装 SAM3 本体 (会强制 numpy<2)
    if [ -d "$ROOT_DIR/mindbridge/models/sam3-main" ]; then
        cd "$ROOT_DIR/mindbridge/models/sam3-main" && pip install -e . && cd "$ROOT_DIR"
    else
        echo "[WARN] mindbridge/models/sam3-main not found, skipping sam3 package install"
    fi

    echo "========== sam3 env ready =========="
}


build_flowpose() {
    if _env_exists flowpose; then
        echo "[SKIP] flowpose already exists"
        return 0
    fi
    set_base
    echo "========== Building flowpose env =========="
    conda create -n flowpose python=$PYTHON_VER -y
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate flowpose

    pip config set global.index-url $MIRROR
    _install_torch

    # FlowPose 核心依赖 (requirements.txt: webdataset, tensorboardX, scikit-learn, zmq)
    pip install opencv-python numpy pyyaml scipy scikit-image scikit-learn zmq webdataset tensorboardX ipdb

    # 服务相关依赖
    pip install uvicorn fastapi pydantic python-multipart

    # 安装 CUDA 编译器完整开发包 (runtime 镜像没有 nvcc 和头文件)
    set +u
    conda install -c nvidia cuda-nvcc cuda-cudart-dev libcublas-dev libcusparse-dev libcufft-dev libcurand-dev libcusolver-dev libnpp-dev -y
    set -u
    export CUDA_HOME="$CONDA_PREFIX"

    # 编译 pointnet2 CUDA 扩展
    cd "$ROOT_DIR/mindbridge/models/flowpose_dino/FlowPose/networks/pts_encoder/pointnet2_utils/pointnet2"
    TORCH_CUDA_ARCH_LIST="7.5;8.0;8.6;8.9+PTX" python setup.py install
    cd "$ROOT_DIR"
    cd "$ROOT_DIR"

    echo "========== flowpose env ready =========="
}

case "${1:-all}" in
    yolo)           build_yolo ;;
    siglip)         build_siglip ;;
    realsense)      build_realsense ;;
    fastfoundation) build_fastfoundation ;;
    sam3)           build_sam3 ;;
    flowpose)       build_flowpose ;;
    all)
        build_yolo
        build_siglip
        build_realsense
        build_fastfoundation
        build_sam3
        build_flowpose
        ;;
    *)
        echo "Usage: $0 [yolo|siglip|realsense|fastfoundation|sam3|flowpose|all]"
        exit 1
        ;;
esac
