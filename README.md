# MindBridge

MindBridge 是一个基于 Docker + Conda 多环境的机器人视觉微服务项目，用 RealSense 采集图像，再连接检测、深度、姿态和状态分类模型。

当前默认管线使用 raw bytes 传输，避免 base64 编解码开销。

---

## Quick Start

```bash
# 1. 宿主机：进入项目并构建 Docker 镜像 / mindtest 命令
cd /home/tjzn-zwt/Aqqqcy/github/kernel-robot
bash build.sh

# 2. 宿主机：进入容器
mindtest

# 3. 容器内：首次构建所有 Conda 环境
bash scripts/build_env.sh all

# 4. 容器内：启动默认完整 SAM3 管线
mind
```

常用启动：

```bash
# 完整管线
mind                         # 默认完整 SAM3: RealSense + FastFoundation + SAM3 + FlowPose + SigLIP
mind --sam3                  # 同上
mind --yolo                  # 完整 YOLO: RealSense + FastFoundation + YOLO + FlowPose + SigLIP

# 基础管线（不启动 FastFoundation / FlowPose）
mind --basic-sam3            # RealSense + SAM3 + SigLIP
mind --basic-yolo            # RealSense + YOLO + SigLIP

# 无窗口 / 限制帧数
mind --sam3 --no-show
mind --basic-yolo --no-show --max-frames 10

# SAM3 自定义提示词
mind --sam3 --sam3-prompts "pen,pencilbag,zipper" --sam3-threshold 0.3

# 只管理服务，不跑主程序
bash scripts/start_service.sh realsense
bash scripts/start_service.sh all
bash scripts/start_service.sh status
bash scripts/start_service.sh stop
```

更新代码后一般不需要重新 `build.sh`，进入容器后重启服务即可：

```bash
bash scripts/start_service.sh stop
bash scripts/start_service.sh all
```

---

## 服务总览

| 服务 | 端口 | Conda 环境 | 功能 |
| --- | --- | --- | --- |
| RealSense | 8000 | `realsense` | 采集 RGB、硬件深度、左右 IR 图像 |
| YOLO | 8001 | `yolo` | 目标检测 / 实例分割 |
| SigLIP | 8002 | `siglip` | 场景 / 状态分类 |
| FastFoundation | 8004 | `fastfoundation` | 双目 IR 深度估计 |
| SAM3 | 8005 | `sam3` | 文本提示驱动的检测 / 分割 |
| FlowPose | 8006 | `flowpose` | 6D 姿态估计 |

常用管线：

```text
完整 SAM3 管线：RealSense → FastFoundation → SAM3 → FlowPose → SigLIP
完整 YOLO 管线：RealSense → FastFoundation → YOLO → FlowPose → SigLIP
基础 SAM3 管线：RealSense → SAM3 → SigLIP
基础 YOLO 管线：RealSense → YOLO → SigLIP
```

---

## 快速开始

### 1. 在宿主机进入项目目录

```bash
cd /home/tjzn-zwt/Aqqqcy/github/kernel-robot
```

### 2. 首次构建 Docker 镜像和 `mindtest` 命令

```bash
bash build.sh
```

`build.sh` 会做两件事：

1. 构建 Docker 镜像 `mindtest`。
2. 安装宿主机命令 `~/.local/bin/mindtest`。

如果提示 PATH 没更新，执行：

```bash
source ~/.bashrc
```

或者直接使用：

```bash
~/.local/bin/mindtest
```

### 3. 进入 Docker 容器

```bash
mindtest
```

必须在项目目录下执行 `mindtest`，因为容器会把当前目录挂载到 `/workspace`：

```bash
-v "$(pwd):/workspace"
```

RealSense 不需要在 Docker 外面单独启动。容器启动时已经带有：

```text
--privileged
-v /dev:/dev
-v /run/udev:/run/udev:ro
--network host
```

所以容器内的 RealSense 服务可以直接访问相机。

### 4. 首次在容器内构建 Conda 环境

进入容器后执行：

```bash
bash scripts/build_env.sh all
```

这一步会创建 6 个 Conda 环境：

```text
yolo
siglip
realsense
fastfoundation
sam3
flowpose
```

同时会在容器内安装 `mind` 启动命令。

以后如果环境已存在，`build_env.sh` 会跳过已有环境。

### 5. 启动默认完整管线

容器内执行：

```bash
mind
```

默认等价于：

```bash
mind --sam3
```

会启动：

```text
RealSense + FastFoundation + SAM3 + FlowPose + SigLIP
```

然后运行：

```bash
python -m mindbridge.src.main --detector sam3 --pipeline full
```

---

## 常用启动命令

以下命令都在 `mindtest` 容器内执行。

### 完整管线

```bash
mind
mind --sam3
```

启动完整 SAM3 管线：

```text
RealSense + FastFoundation + SAM3 + FlowPose + SigLIP
```

```bash
mind --yolo
```

启动完整 YOLO 管线：

```text
RealSense + FastFoundation + YOLO + FlowPose + SigLIP
```

### 基础管线

基础管线不启动 FastFoundation 和 FlowPose。

```bash
mind --basic-sam3
```

启动：

```text
RealSense + SAM3 + SigLIP
```

```bash
mind --basic-yolo
```

启动：

```text
RealSense + YOLO + SigLIP
```

### 无窗口运行

如果远程机器没有 GUI，给 `mind` 后面的主程序透传 `--no-show`：

```bash
mind --sam3 --no-show
mind --basic-yolo --no-show
```

限制帧数：

```bash
mind --basic-yolo --no-show --max-frames 10
```

自定义 SAM3 prompt：

```bash
mind --sam3 --sam3-prompts "pen,pencilbag,zipper" --sam3-threshold 0.3
```

### 查看帮助

```bash
mind --help
```

---

## 单独启动服务

推荐用 `scripts/start_service.sh` 管理服务。

```bash
bash scripts/start_service.sh realsense
bash scripts/start_service.sh yolo
bash scripts/start_service.sh siglip
bash scripts/start_service.sh fastfoundation
bash scripts/start_service.sh sam3
bash scripts/start_service.sh flowpose
```

启动所有服务：

```bash
bash scripts/start_service.sh all
```

查看状态：

```bash
bash scripts/start_service.sh status
```

停止所有服务：

```bash
bash scripts/start_service.sh stop
```

重启所有服务：

```bash
bash scripts/start_service.sh restart
```

服务日志在：

```text
logs/realsense.log
logs/yolo.log
logs/siglip.log
logs/fastfoundation.log
logs/sam3.log
logs/flowpose.log
```

PID 文件在：

```text
/tmp/mindbridge/*.pid
```

注意：`mind --rs-only` 当前脚本会先启动 RealSense，然后继续运行主程序；如果只想启动 RealSense 服务，不跑主程序，使用：

```bash
bash scripts/start_service.sh realsense
```

## API 接口

所有服务均提供：

```text
GET /health
GET /docs
```

### RealSense

Base64 兼容接口：

```text
POST http://127.0.0.1:8000/realsense/capture
```

Raw bytes 接口：

```text
POST http://127.0.0.1:8000/realsense/capture/raw
```
### YOLO

Raw bytes 接口：

```text
POST http://127.0.0.1:8001/infer/predict/raw
```

Base64 兼容接口：

```text
POST http://127.0.0.1:8001/infer/predict
```

### SigLIP

Raw bytes 接口：

```text
POST http://127.0.0.1:8002/infer/predict/raw
```

### FastFoundation

Raw bytes 接口：

```text
POST http://127.0.0.1:8004/infer/stereo/raw
```

Base64 兼容接口：

```text
POST http://127.0.0.1:8004/infer/stereo
```

### SAM3

Raw bytes 接口：

```text
POST http://127.0.0.1:8005/infer/detect/raw
```

Base64 兼容接口：

```text
POST http://127.0.0.1:8005/infer/detect
```

### FlowPose

Raw bytes 接口：

```text
POST http://127.0.0.1:8006/infer/pose/raw
```

---

## 更新代码后是否需要重新 build

如果只是在同一台机器上 `git pull` 更新代码，通常不需要重新执行：

```bash
bash build.sh
```

原因是 `mindtest` 容器把宿主机当前项目目录挂载到 `/workspace`，代码更新后容器内能直接看到新代码。

更新代码后一般只需要在容器内重启服务：

```bash
bash scripts/start_service.sh stop
bash scripts/start_service.sh all
```

以下情况才需要重新执行 `build.sh`：

1. 新机器第一次部署。
2. Docker 镜像 `mindtest` 不存在。
3. 宿主机命令 `mindtest` 不存在。
4. Dockerfile 发生变化，并且需要更新镜像系统依赖。

以下情况需要重新执行 `scripts/build_env.sh`：

1. 删除过 `mindtest` 容器，Conda 环境丢失。
2. 新增或修改了模型环境依赖。
3. 某个 Conda 环境不存在。

---

## 容器管理

进入容器：

```bash
mindtest
```

等价的 Docker 命令：

```bash
docker start mindtest
docker exec -it mindtest bash
```

停止容器：

```bash
docker stop mindtest
```

删除容器：

```bash
docker rm -f mindtest
```

删除容器会丢失容器内 Conda 环境；下次需要重新执行：

```bash
bash scripts/build_env.sh all
```

---

## 目录结构

```text
.
├── build.sh                         # 宿主机构建 Docker 镜像并安装 mindtest
├── Dockerfile                       # Docker 镜像定义
├── bin/
│   └── mind                         # 容器内管线启动命令
├── scripts/
│   ├── build_env.sh                 # 构建 Conda 环境
│   └── start_service.sh             # 启停 FastAPI 服务
├── mindbridge/
│   ├── src/
│   │   ├── main.py                  # Control Center 主程序
│   │   ├── MindBridgeClient.py      # 服务客户端
│   │   └── core/
│   │       ├── config/              # 服务配置
│   │       ├── controller/          # FastAPI 路由
│   │       ├── launch/              # 服务入口
│   │       ├── schemas/             # Pydantic 实体
│   │       ├── service/             # 相机 / 模型服务封装
│   │       └── tool/                # 工具函数
│   └── models/                      # 模型代码和权重
└── logs/                            # 服务日志
```
