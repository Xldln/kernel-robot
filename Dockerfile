FROM nvcr.io/nvidia/cuda:12.8.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://mirrors.aliyun.com/ubuntu/|g' /etc/apt/sources.list \
    && sed -i 's|http://security.ubuntu.com/ubuntu/|http://mirrors.aliyun.com/ubuntu/|g' /etc/apt/sources.list \
    && sed -i 's|http://ports.ubuntu.com/ubuntu-ports/|http://mirrors.aliyun.com/ubuntu-ports/|g' /etc/apt/sources.list || true

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    wget \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libusb-1.0-0 \
    libgl1 \
    libgl1-mesa-glx \
    libx11-6 \
    libx11-dev \
    libgtk-3-0 \
    python3-tk \
    libudev1 \
    udev \
    && rm -rf /var/lib/apt/lists/*

ENV CONDA_DIR=/opt/conda
RUN wget -O /tmp/miniconda.sh \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash /tmp/miniconda.sh -b -p $CONDA_DIR \
    && rm /tmp/miniconda.sh

ENV PATH=$CONDA_DIR/bin:$PATH


RUN conda init bash \
    && conda config --set auto_activate_base true \
    && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ \
    && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \
    && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ \
    && conda config --set show_channel_urls yes \
    && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main \
    && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r \
    && conda install python=3.12 -y \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install pillow uvicorn fastapi numpy opencv-python \
    && pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu128 


WORKDIR /workspace
COPY . /workspace
