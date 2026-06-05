# MindBridge

## 功能

- RealSense RGB、硬件深度、左右 IR 采集。
- YOLO 或 SAM3 检测 / 分割管线。
- FastFoundation 双目深度估计。
- FlowPose 6D 姿态估计。
- SigLIP 场景 / 状态分类。
- Docker 一键进入环境，脚本统一管理各个微服务。

## 快速开始

在仓库根目录执行：

```bash
# 构建 Docker 镜像，并安装宿主机命令 mindtest
bash build.sh

# 进入容器
mindtest

# 在容器内构建全部 Conda 环境
bash scripts/build_env.sh all

# 启动默认完整 SAM3 管线
mind
```

`mind` 默认等价于：

```text
RealSense -> FastFoundation -> SAM3 -> FlowPose -> SigLIP
```

## 常用命令

以下命令均在 `mindtest` 容器内执行。

```bash
# 完整管线
mind                         # 等价于 mind --sam3
mind --sam3                  # RealSense + FastFoundation + SAM3 + FlowPose + SigLIP
mind --yolo                  # RealSense + FastFoundation + YOLO + FlowPose + SigLIP

# 基础管线
mind --basic-sam3            # RealSense + SAM3 + SigLIP
mind --basic-yolo            # RealSense + YOLO + SigLIP

# 无窗口 / 限制帧数
mind --sam3 --no-show
mind --basic-yolo --no-show --max-frames 10

# SAM3 自定义提示词
mind --sam3 --sam3-prompts "pen,pencilbag,zipper" --sam3-threshold 0.3

# 查看帮助
mind --help
```

## 服务

| 服务 | 端口 | Conda 环境 | 功能 |
| --- | ---: | --- | --- |
| RealSense | 8000 | `realsense` | RGB、深度、左右 IR 采集 |
| YOLO | 8001 | `yolo` | 目标检测 / 实例分割 |
| SigLIP | 8002 | `siglip` | 场景 / 状态分类 |
| FastFoundation | 8004 | `fastfoundation` | 双目 IR 深度估计 |
| SAM3 | 8005 | `sam3` | 文本提示驱动的检测 / 分割 |
| FlowPose | 8006 | `flowpose` | 6D 姿态估计 |

单独管理服务：

```bash
bash scripts/start_service.sh all
bash scripts/start_service.sh status
bash scripts/start_service.sh stop
bash scripts/start_service.sh restart

bash scripts/start_service.sh realsense
bash scripts/start_service.sh yolo
bash scripts/start_service.sh siglip
bash scripts/start_service.sh fastfoundation
bash scripts/start_service.sh sam3
bash scripts/start_service.sh flowpose
```

日志位于 `logs/*.log`，PID 文件位于 `/tmp/mindbridge`。

## API

所有服务都提供：

```text
GET /health
GET /docs
```

主要推理接口：

| 服务 | 接口 |
| --- | --- |
| RealSense | `POST /realsense/capture/raw` |
| YOLO | `POST /infer/predict/raw` |
| SigLIP | `POST /infer/predict/raw` |
| FastFoundation | `POST /infer/stereo/raw` |
| SAM3 | `POST /infer/detect/raw` |
| FlowPose | `POST /infer/pose/raw` |

RealSense、YOLO、FastFoundation 和 SAM3 也保留 base64 兼容接口。实际运行建议优先使用 raw 接口。

## 目录结构

```text## 更新代码

项目代码会挂载到容器的 `/workspace`，普通代码更新通常不需要重新构建 Docker
镜像。更新后重启服务即可：

```bash
bash scripts/start_service.sh stop
bash scripts/start_service.sh all
```

只有 Docker 镜像或宿主机 `mindtest` 命令需要重建时，才重新执行 `bash build.sh`。
Conda 环境缺失或依赖变更时，重新执行 `bash scripts/build_env.sh all`。
.
├── build.sh                    # 构建 Docker 镜像并安装 mindtest
├── Dockerfile                  # CUDA + Miniconda 运行环境
├── bin/mind                    # 容器内管线启动命令
├── scripts/
│   ├── build_env.sh            # 构建 Conda 环境
│   └── start_service.sh        # 启停 FastAPI 服务
├── mindbridge/
│   ├── src/main.py             # Control Center 主循环
│   ├── src/MindBridgeClient.py # 服务客户端
│   └── src/core/               # config、launch、controller、service、schemas、tool
└── logs/                       # 服务日志
```

## 更新代码

项目代码会挂载到容器的 `/workspace`，普通代码更新通常不需要重新构建 Docker
镜像。更新后重启服务即可：

```bash
bash scripts/start_service.sh stop
bash scripts/start_service.sh all
```

只有 Docker 镜像或宿主机 `mindtest` 命令需要重建时，才重新执行 `bash build.sh`。
Conda 环境缺失或依赖变更时，重新执行 `bash scripts/build_env.sh all`。
