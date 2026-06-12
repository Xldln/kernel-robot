# MindBridge / TJfusion

当前推荐部署方式：**一个主镜像 `tjfusion:latest`，一个主容器 `TJfusion`，所有 MindBridge 服务都在这个容器里运行**。

旧的 `mindtest` 容器可以保留，但不要和 `TJfusion` 同时跑 MindBridge 服务，否则会抢占 `8000-8006` 端口。

## 快速启动

在仓库根目录执行：

```bash
./run.sh
```

网页地址：

```text
http://127.0.0.1:8765
```

进入容器：

```bash
tjfusion
```

等价于：

```bash
docker exec -it TJfusion bash
```

## 管线命令

以下命令在 `TJfusion` 容器内执行。

```bash
mind                         # 默认 SAM3 Full
mind --sam3                  # RealSense + FastFoundation + SAM3 + FlowPose + SigLIP
mind --yolo                  # RealSense + FastFoundation + YOLO + FlowPose + SigLIP
mind --basic-sam3
mind --basic-yolo
mind --yolo-only
mind --sam3-only
mind --siglip-only
mind --flowpose-only
mind --rs-only
```

## 服务管理

```bash
bash scripts/start_service.sh status     # 查看服务状态
bash scripts/start_service.sh all        # 启动全部服务
bash scripts/start_service.sh yolo-full  # 启动 YOLO Full 依赖
bash scripts/start_service.sh sam3-full  # 启动 SAM3 Full 依赖
bash scripts/start_service.sh stop       # 停止全部服务
```

服务端口：

| 服务 | 端口 |
| --- | ---: |
| RealSense | 8000 |
| YOLO | 8001 |
| SigLIP | 8002 |
| FastFoundation | 8004 |
| SAM3 | 8005 |
| FlowPose | 8006 |
| Fusion Web UI | 8765 |

## RealSense

RealSense 需要同时满足：

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/realsense/info
```

`/realsense/info` 正常返回相机内参才表示相机 engine 可用。

## FlowPose 可视化

窗口大小配置：

```text
mindbridge/src/core/config/flowpose-config.yaml
```

当前默认：

```yaml
window_width: 640
window_height: 480
```

窗口聚焦时按 `ESC` 或 `q` 会关闭可视化窗口，但不会停止 FlowPose 服务。

接口关闭：

```bash
curl -X POST 'http://127.0.0.1:8006/infer/visualization?enabled=false'
```

接口打开：

```bash
curl -X POST 'http://127.0.0.1:8006/infer/visualization?enabled=true'
```

## Docker 说明

`TJfusion` 是容器名，不是镜像名。

```bash
docker ps
docker images
```

如果 `docker ps` 里 `TJfusion` 的 IMAGE 显示为 `f759...` 这类镜像 ID，说明容器创建时使用的是镜像 ID。功能不受影响。要显示 `tjfusion:latest`，需要重建容器对象，但不需要删除镜像。

`mindtest` 现在只作为旧环境保留。不要让它和 `TJfusion` 同时跑服务。
