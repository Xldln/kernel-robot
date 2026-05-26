# MindBridge


## 目录结构

```
MindBridge/
├── mindbridge/
│   └── src/
│       ├── main.py                    # FastAPI 入口，loguru 日志，CORS
│       └── core/
│           ├── schemas/               # Pydantic 请求/响应模型
│           │   └── YoloEntity.py      #   PredictRequest, PredictResponse, Detection
│           ├── tool/                  # 通用工具
│           │   └── image.py           #   ImageProcessor (base64 编解码)
│           ├── client/                # 对外 HTTP 客户端
│           │   ├── InstanceSegment.py #   InstanceSegmentClient (httpx)
│           │   └── StatusCls.py
│           ├── service/               # 业务逻辑（YOLO 推理）
│           │   └── InstanceSegmentInfer.py
│           ├── controller/            # FastAPI 路由
│           │   └── InstanceSegController.py
│           └── config/                # 配置
├── models/
│   ├── config/                        # 模型配置 (yaml)
│   └── weights/                       # 模型权重
├── Dockerfile                         # CUDA 12.8 + Miniconda
├── build.sh                           # 构建镜像 + 安装 mindbridge 命令
├── run.sh                             # 快速启动容器
├── pyproject.toml                     # 项目元数据
└── tests/
```

## 分层说明

| 层 | 职责 |
|----|------|
| `controller/` | FastAPI 路由，HTTP 接口层 |
| `service/`    | YOLO 推理逻辑 |
| `client/`     | 供外部服务调用的 HTTP 客户端 |
| `schemas/`    | Pydantic 模型（请求/响应约定） |
| `tool/`       | 共享工具（图片编解码等） |

## 快速开始

```bash
# 构建镜像并安装 CLI
./build.sh

# 进入容器
mindbridge
```
