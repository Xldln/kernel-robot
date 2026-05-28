# MindBridge

YOLO 实例分割 + RealSense 深度估计的微服务架构。

## 目录结构

```
MindBridge/
├── mindbridge/                          # Python 包
│   ├── main.py                          # 一体化 FastAPI (端口 6666, 整合控制+自动采集)
│   │
│   ├── src/core/
│   │   ├── launch/                      # ══ 服务入口 ══
│   │   │   ├── service_InsenceSeg.py    #   YOLO 推理服务      → :8001
│   │   │   └── service_RealSense.py     #   RealSense 深度服务  → :8000
│   │   │
│   │   ├── controller/                  # ══ FastAPI 路由 ══
│   │   │   ├── Controlcenter.py         #   相机采集启动/停止
│   │   │   ├── InstanceSegController.py #   YOLO /predict, /predict/file
│   │   │   └── RealSenseController.py   #   RealSense /capture, /info, /shutdown
│   │   │
│   │   ├── service/                     # ══ 业务逻辑 ══
│   │   │   ├── InstanceSegmentInfer.py  #   YOLOInfer – 模型加载、推理
│   │   │   └── RealsenseService.py      #   RealsenseService – 相机、立体深度
│   │   │
│   │   ├── schemas/                     # ══ Pydantic 模型 ══
│   │   │   ├── YoloEntity.py            #   PredictRequest, PredictResponse, Detection
│   │   │   └── RealsenseEntity.py       #   CaptureRequest/Response, CameraInfo, Shutdown
│   │   │
│   │   ├── tool/                        # ══ 通用工具 ══
│   │   │   └── image.py                 #   base64 <-> numpy 编解码
│   │   │
│   │   └── config/                      # ══ YAML 配置文件 ══
│   │       ├── yolo-config.yaml         #   YOLO 模型路径、置信度阈值
│   │       ├── realsense-config.yaml    #   相机分辨率、FoundationStereo 参数
│   │       └── last-vit-config.yaml     #   (遗留)
│   │
│   └── models/
│       ├── config/                      # YOLO 数据集/模型 YAML
│       ├── weights/yolo/                # 训练好的 .pt 权重文件
│       └── pkg/yolo/                    # Ultralytics 源码 (pip install -e .)
│
├── scripts/                             # ══ 运维脚本 ══
│   ├── build_env.sh                     #   创建 conda 环境 (yolo / realsense)
│   └── start_service.sh                 #   启动 / 停止 / 查看服务状态
│
├── tests/                               # 测试占位
├── logs/                                # 服务日志 (自动创建)
│
├── Dockerfile                           # CUDA 12.8 + Miniconda + libusb
├── pyproject.toml                       # 项目元数据, ruff, pytest
├── README.md
└── README-zh.md
```

## 架构

每个微服务是一个自包含的 FastAPI 应用，分为三层：

| 层           | 职责                             |
|--------------|----------------------------------|
| `launch/`    | FastAPI 应用、生命周期、端口绑定 |
| `controller/` | APIRouter、HTTP 接口、Schema 校验 |
| `service/`   | 核心业务逻辑（模型推理、相机）   |

**设计原则**：`launch/` → `controller/` → `service/` & `schemas/`，禁止反向依赖。包 `__init__.py` 刻意为空，避免拉入无关的设备级依赖。

## 服务

| 服务              | 端口 | Conda 环境    | 依赖                                          |
|-------------------|------|---------------|-----------------------------------------------|
| YOLO 实例分割     | 8001 | `yolo`        | torch, ultralytics, opencv, fastapi           |
| RealSense 深度    | 8000 | `realsense`   | torch, pyrealsense2, omegaconf, opencv, fastapi |

## 快速开始

```bash

# 构建镜像并安装 CLI
./build.sh

# 进入容器
mindbridge

# 构建环境
bash scripts/build_env.sh yolo       # 或 realsense / all

# 启动服务
bash scripts/start_service.sh yolo   # 或 realsense / all / stop / status

# 测试
curl http://localhost:8001/health
curl http://localhost:8001/infer/predict -X POST -H "Content-Type: application/json" -d '{"image_b64":"..."}'
```
