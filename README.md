# MindBridge

Microservice architecture for YOLO instance segmentation + RealSense depth estimation.

## Directory Structure

```
MindBridge/
├── mindbridge/                          # Python package
│   ├── main.py                          # All-in-one FastAPI (port 6666, control + auto-start)
│   │
│   ├── src/core/
│   │   ├── launch/                      # ══ Service entry points ══
│   │   │   ├── service_InsenceSeg.py    #   YOLO inference       → :8001
│   │   │   └── service_RealSense.py     #   RealSense depth      → :8000
│   │   │
│   │   ├── controller/                  # ══ FastAPI routers ══
│   │   │   ├── Controlcenter.py         #   Camera capture start/stop
│   │   │   ├── InstanceSegController.py #   YOLO /predict, /predict/file
│   │   │   └── RealSenseController.py   #   RealSense /capture, /info, /shutdown
│   │   │
│   │   ├── service/                     # ══ Business logic ══
│   │   │   ├── InstanceSegmentInfer.py  #   YOLOInfer – model loading, predict
│   │   │   └── RealsenseService.py      #   RealsenseService – camera, stereo depth
│   │   │
│   │   ├── schemas/                     # ══ Pydantic models ══
│   │   │   ├── YoloEntity.py            #   PredictRequest, PredictResponse, Detection
│   │   │   └── RealsenseEntity.py       #   CaptureRequest/Response, CameraInfo, Shutdown
│   │   │
│   │   ├── tool/                        # ══ Shared utilities ══
│   │   │   └── image.py                 #   base64 <-> numpy, encode/decode
│   │   │
│   │   └── config/                      # ══ YAML configurations ══
│   │       ├── yolo-config.yaml         #   YOLO model path, score threshold
│   │       ├── realsense-config.yaml    #   Camera resolution, FoundationStereo params
│   │       └── last-vit-config.yaml     #   (legacy)
│   │
│   └── models/
│       ├── config/                      # YOLO dataset/model YAMLs
│       ├── weights/yolo/                # Trained .pt weight files
│       └── pkg/yolo/                    # Ultralytics source (pip install -e .)
│
├── scripts/                             # ══ DevOps ══
│   ├── build_env.sh                     #   Create conda environments (yolo / realsense)
│   └── start_service.sh                 #   Start / stop / status of services
│
├── tests/                               # Test stubs
├── logs/                                # Service stdout (auto-created)
│
├── Dockerfile                           # CUDA 12.8 + Miniconda + libusb
├── pyproject.toml                       # Project metadata, ruff, pytest
├── README.md
└── README-zh.md
```

## Architecture

Each microservice is a self-contained FastAPI application with a three-layer structure:

| Layer        | Responsibility                              |
|--------------|---------------------------------------------|
| `launch/`    | FastAPI app, lifespan, port binding         |
| `controller/` | APIRouter, HTTP interface, schema validation |
| `service/`   | Core business logic (model inference, camera) |

**Key design rule**: `launch/` imports from `controller/`, `controller/` imports from `service/` and `schemas/`. No reverse dependencies. Package `__init__.py` files are intentionally empty to avoid pulling in device-specific dependencies.

## Services

| Service       | Port | Conda Env     | Dependencies                                    |
|---------------|------|---------------|-------------------------------------------------|
| YOLO InstanceSeg | 8001 | `yolo`     | torch, ultralytics, opencv, fastapi             |
| RealSense Depth  | 8000 | `realsense` | torch, pyrealsense2, omegaconf, opencv, fastapi |

## Quick Start

```bash

# Build image and install CLI
./build.sh

# Enter container
mindbridge

# Build environment
bash scripts/build_env.sh yolo       # or: realsense / all

# Start service
bash scripts/start_service.sh yolo   # or: realsense / all / stop / status

# Test
curl http://localhost:8001/health
curl http://localhost:8001/infer/predict -X POST -H "Content-Type: application/json" -d '{"image_b64":"..."}'
```
