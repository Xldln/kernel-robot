# MindBridge



## Architecture

```
MindBridge/
├── mindbridge/
│   └── src/
│       ├── main.py                    # FastAPI entry point, loguru, CORS
│       └── core/
│           ├── schemas/               # Pydantic request/response models
│           │   └── YoloEntity.py      #   PredictRequest, PredictResponse, Detection
│           ├── tool/                  # Common utilities
│           │   └── image.py           #   ImageProcessor (base64 encode/decode)
│           ├── client/                # HTTP clients for external callers
│           │   ├── InstanceSegment.py #   InstanceSegmentClient (httpx)
│           │   └── StatusCls.py
│           ├── service/               # Business logic (YOLO inference)
│           │   └── InstanceSegmentInfer.py
│           ├── controller/            # FastAPI routers
│           │   └── InstanceSegController.py
│           └── config/                # Configuration
├── models/
│   ├── config/                        # Model configs (yaml)
│   └── weights/                       # Model weights
├── Dockerfile                         # CUDA 12.8 + Miniconda
├── build.sh                           # Build image + install mindbridge CLI
├── run.sh                             # Quick start container
├── pyproject.toml                     # Project metadata
└── tests/
```

## Layers

| Layer | Role |
|-------|------|
| `controller/` | FastAPI routes, HTTP interface |
| `service/`    | YOLO inference logic |
| `client/`     | HTTP client library for external services |
| `schemas/`    | Pydantic models (request/response contract) |
| `tool/`       | Shared utilities (image encoding, etc.) |

## Quick Start

```bash
# Build image and install CLI
./build.sh

# Enter container
mindbridge
```
