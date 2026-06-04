# MindBridge

多模型微服务架构：目标检测 / 姿态估计 / 状态分类 / 深度估计。

---

## 服务总览

| 服务 | 端口 | 功能 | 管线 |
|------|------|------|------|
| RealSense | 8000 | 相机采集 RGB+深度+红外 | 必用 |
| YOLO | 8001 | 实例检测/分割 | YOLO/basic |
| SigLIP | 8002 | 场景状态分类 | 必用 |
| FastFoundation | 8004 | 双目深度估计 | full 管线 |
| SAM3 | 8005 | 文本驱动的检测/分割 | SAM3/basic |
| FlowPose | 8006 | 6D 姿态估计 | full 管线 |

---

## 快速开始

```bash
# 1. 构建镜像（仅首次）
cd /home/kewei/github/kernel-robot-test
docker build -t mindtest .

# 2. 启动容器（仅首次）
docker run --gpus all -itd \
  -v $(pwd):/workspace \
  --name mindtest \
  mindtest bash

# 3. 进入容器
docker exec -it mindtest bash

# 4. 安装环境（仅首次）
bash scripts/build_env.sh all

# 5. 启动管线 (默认完整 SAM3)
mind            # 完整管线: RealSense + FF + SAM3 + FlowPose + SigLIP
```

> **之后每次使用** 只需 `docker start mindtest` + `docker exec -it mindtest bash` + `mind`

---

## 命令详解

### `mind` 命令

```bash
# 默认 = 完整 SAM3 管线
mind              # 完整 SAM3:  RealSense + FF + SAM3 + FlowPose + SigLIP
mind --sam3       # 同上
mind --yolo       # 完整 YOLO:  RealSense + FF + YOLO + FlowPose + SigLIP

# 基础管线 (无 FastFoundation / FlowPose)
mind --basic-sam3   # 基础 SAM3:  RealSense + SAM3 + SigLIP
mind --basic-yolo   # 基础 YOLO:  RealSense + YOLO + SigLIP

# 单独服务
mind --yolo-only     # 只启动 YOLO
mind --siglip-only   # 只启动 SigLIP
mind --rs-only       # 只启动 RealSense
```

### `bash scripts/start_service.sh`

```bash
bash scripts/start_service.sh all        # 启动所有服务
bash scripts/start_service.sh yolo       # 启动单个服务
bash scripts/start_service.sh sam3
bash scripts/start_service.sh stop       # 停止所有服务
bash scripts/start_service.sh status     # 查看运行状态
bash scripts/start_service.sh restart    # 重启所有服务
```

### `bash scripts/build_env.sh`

```bash
bash scripts/build_env.sh all      # 安装全部 6 个环境
bash scripts/build_env.sh sam3     # 安装单个环境
bash scripts/build_env.sh yolo siglip realsense   # 安装多个
```

### `bash scripts/test_*.sh`

```bash
bash scripts/test_sam3.sh           # SAM3 测试 (health + 推理)
bash scripts/test_fastfoundation.sh # FastFoundation 测试
bash scripts/test_flowpose.sh       # FlowPose 测试
```

---

## 管线说明

```
完整管线 (默认 mind / mind --sam3 / mind --yolo):
  RealSense → FastFoundation (深度) → SAM3/YOLO (检测+mask) → FlowPose (6D姿态) → SigLIP (分类)

基础管线 (mind --basic-sam3 / --basic-yolo):
  RealSense → SAM3/YOLO (检测) → SigLIP (分类)

---

## SAM3 自定义 Prompt

```bash
mind --sam3 --sam3-prompts "pen,pencilbag,zipper" --sam3-threshold 0.3
```

不传 `--sam3-prompts` 默认 `["object"]`，`--sam3-threshold` 默认用服务端配置 (0.4)。

---

## API 接口

### YOLO
```bash
POST http://127.0.0.1:8001/infer/predict
{"request_id": "...", "image_b64": "...", "return_annotated_image": true}
```

### SAM3
```bash
POST http://127.0.0.1:8005/infer/detect
{"request_id": "...", "image_b64": "...", "prompts": ["pen"], "score_threshold": 0.3}
```

### SigLIP
```bash
POST http://127.0.0.1:8002/infer/predict
{"request_id": "...", "image_b64": "..."}
```

### FastFoundation
```bash
POST http://127.0.0.1:8004/infer/stereo
{"request_id": "...", "left_image_b64": "...", "right_image_b64": "...", "return_depth": true}
```

### FlowPose
```bash
POST http://127.0.0.1:8006/infer/pose
{"request_id": "...", "rgb_image": "...", "depth_image": "...", "combined_mask": "...", "obj_ids": [[1,1]], "class_names": ["pen"]}
```

所有服务均有 `GET /health` 和 `Swagger UI /docs`。

---

## 容器管理

```bash
docker start mindtest          # 启动已有容器（环境不丢）
docker stop mindtest           # 停止容器
docker exec -it mindtest bash  # 进入容器
docker rm -f mindtest          # 删除容器（⚠️ 环境丢失，需重建）
```

> **重要**: 永远用 `docker start` 而不是 `docker run`，否则 conda 环境丢失。

---

## 目录结构

```
mindbridge/
├── bin/mind                        # 启动命令
├── scripts/
│   ├── build_env.sh                # 环境构建
│   ├── start_service.sh            # 服务管理
│   ├── test_sam3.sh                # SAM3 测试
│   ├── test_fastfoundation.sh      # FastFoundation 测试
│   └── test_flowpose.sh            # FlowPose 测试
├── mindbridge/src/core/
│   ├── config/                     # 6 个 YAML 配置文件
│   │   ├── yolo-config.yaml
│   │   ├── siglip-config.yaml
│   │   ├── sam3-config.yaml
│   │   ├── fastfoundation-config.yaml
│   │   ├── flowpose-config.yaml
│   │   └── realsense-config.yaml
│   ├── schemas/                    # Pydantic 实体
│   ├── tool/                       # 工具函数
│   ├── service/                    # 推理引擎 (Infer)
│   ├── controller/                 # FastAPI 路由
│   ├── launch/                     # 服务入口 (service_*.py)
│   └── main.py                     # Control Center 管线
├── mindbridge/models/
│   ├── sam3-main/                  # SAM3 代码
│   ├── siglip2-so400m-patch14-224/ # SigLIP 代码
│   ├── Fast-FoundationStereo-master/ # FastFoundation 代码
│   ├── flowpose_dino/              # FlowPose + DINOv2 代码
│   ├── pkg/yolo/                   # YOLO 包
│   └── weights/                    # 所有权重文件
│       ├── yolo/
│       ├── siglip/
│       ├── sam3/
│       ├── fastfoundation/
│       └── flowpose_dino/
├── Dockerfile
└── .dockerignore
```
