# MindBridge / TJfusion

MindBridge 是一套面向 RealSense + 视觉模型 + 机器人执行的本地推理管线。推荐部署方式：**一个主镜像 `tjfusion:latest`，一个主容器 `TJfusion`，所有 MindBridge 服务都在这个容器里运行**。

## 架构

```text
TJfusion 容器
├── Fusion Web UI              :8765
├── RealSense 服务             :8000
├── YOLO 服务                  :8001
├── SigLIP 服务                :8002
├── FastFoundation 服务        :8004
├── SAM3 服务                  :8005
└── FlowPose 服务              :8006
```

服务日志：

```text
logs/*.log
```

服务 PID 在容器内：

```text
/tmp/mindbridge/*.pid
```

## 快速启动

在仓库根目录运行：

```bash
./run.sh
```

打开网页：

```text
http://127.0.0.1:8765
```

`./run.sh` 会启动或复用 `TJfusion` 容器，并在容器里启动 Fusion Web UI。

## 进入容器

推荐直接输入：

```bash
tjfusion
```

等价于：

```bash
docker exec -it TJfusion bash
```

如果提示 `tjfusion` 命令不存在，确认 `~/.local/bin` 在 `PATH` 中：

```bash
echo "$PATH"
```

## 常用管线

以下命令在 `TJfusion` 容器内执行。

```bash
mind
```

默认启动完整 SAM3 管线：

```text
RealSense + FastFoundation + SAM3 + FlowPose + SigLIP
```

启动完整 YOLO 管线：

```bash
mind --yolo
```

启动基础管线（不含 FastFoundation + FlowPose）：

```bash
mind --basic-sam3
mind --basic-yolo
```

单独模式：

```bash
mind --yolo-only
mind --sam3-only
mind --siglip-only
mind --flowpose-only
mind --rs-only
```

无窗口运行：

```bash
mind --yolo --no-show
```

### 附加参数

所有管线命令均支持传递附加参数：

```bash
mind --show                         # 显示 OpenCV 窗口（默认）
mind --no-show                      # 无头模式，不显示窗口
mind --rgb-source usb               # 使用 USB RGB 摄像头而非 RealSense
mind --fusion-pub                   # 发布 Fusion ZMQ 结果到 :8899
mind --fusion-ui-url http://127.0.0.1:8765  # 推送视频帧到 Fusion UI
```

## 多相机模式（Multi-Camera）

当 RealSense 连接了多个相机（1 个 primary + N 个 aux color-only 相机）时，使用 `--camera-mode multi` 启用多相机采集：

```bash
mind --camera-mode multi
```

在此模式下：
- **Primary 相机**：完整采集 color + depth + IR（用于检测、深度估计、姿态估计）
- **Aux 相机**：只采集彩色帧（用于丰富 SigLIP 多视角状态识别）
- **SigLIP**：将所有相机的彩色帧横向拼接为一张多视角图，进行联合状态分类，提升分类准确率
- **可视化**：会额外弹出一个 `SigLIP MultiView` 窗口，展示各相机视角的拼接画面

仅使用单相机（默认）：

```bash
mind --camera-mode single
```

注意：`multi` 模式仅适用于 `--rgb-source realsense`（默认）。USB 摄像头不支持多相机模式。

## 服务管理

在 `TJfusion` 容器内执行：

```bash
bash scripts/start_service.sh status
bash scripts/start_service.sh yolo-full          # YOLO 完整管线依赖
bash scripts/start_service.sh sam3-full          # SAM3 完整管线依赖
bash scripts/start_service.sh basic-yolo         # YOLO 基础管线依赖
bash scripts/start_service.sh basic-sam3         # SAM3 基础管线依赖
bash scripts/start_service.sh flowpose-stack     # FlowPose 管线依赖
bash scripts/start_service.sh all                # 所有服务
bash scripts/start_service.sh stop               # 停止所有
bash scripts/start_service.sh restart            # 重启所有
```

单独启动某个服务：

```bash
bash scripts/start_service.sh realsense
bash scripts/start_service.sh yolo
bash scripts/start_service.sh sam3
bash scripts/start_service.sh siglip
bash scripts/start_service.sh fastfoundation
bash scripts/start_service.sh flowpose
```

## RealSense 检查

RealSense 不只要 `/health` 正常，还要相机 engine 正常：

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/realsense/info
```

正常时 `/realsense/info` 会返回相机内参。  
如果出现 `engine_missing` 或 `Engine not initialized`，需要重启 RealSense 服务：

```bash
bash scripts/start_service.sh realsense
```

## FlowPose 可视化

FlowPose 可视化窗口大小配置在：

```text
mindbridge/src/core/config/flowpose-config.yaml
```

当前默认：

窗口聚焦时按 `ESC` 或 `q` 会关闭 FlowPose 可视化窗口，但不会停止 FlowPose 服务。

也可以用接口关闭：

```bash
curl -X POST 'http://127.0.0.1:8006/infer/visualization?enabled=false'
```

重新打开：

```bash
curl -X POST 'http://127.0.0.1:8006/infer/visualization?enabled=true'
```

## Docker 说明

查看运行中的容器：

```bash
docker ps
```

你应该看到：

```text
TJfusion
```

`TJfusion` 是容器名，不是镜像名。  
`docker images` 显示的是镜像，例如：

```text
tjfusion:latest
```

如果 `docker ps` 里 `TJfusion` 的 IMAGE 显示成镜像 ID，例如 `f759...`，说明这个容器创建时使用的是镜像 ID。功能不受影响。要让它显示 `tjfusion:latest`，需要重建容器，但不需要删除镜像。

## 更新代码

代码挂载到容器的 `/workspace`。普通代码修改后通常不需要重建镜像，只需要重启相关服务：

```bash
bash scripts/start_service.sh stop
bash scripts/start_service.sh yolo-full
```

只有镜像依赖、Conda 环境或系统包变化时，才需要重建镜像或重新构建环境。
