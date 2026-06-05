# MindBridge
## Features

- RealSense RGB, hardware depth, and stereo IR capture.
- YOLO or SAM3 detection/segmentation pipelines.
- FastFoundation stereo depth estimation.
- FlowPose 6D pose estimation.
- SigLIP scene/state classification.
- One-command Docker entry plus per-service process management.
## Quick Start

Run these commands from the repository root.

```bash
# Build the Docker image and install the host command: mindtest
bash build.sh

# Enter the container
mindtest

# Build all Conda environments inside the container
bash scripts/build_env.sh all

# Start the default full SAM3 pipeline
mind
```

`mind` defaults to:

```text
RealSense -> FastFoundation -> SAM3 -> FlowPose -> SigLIP
```

## Common Commands

All commands below run inside the `mindtest` container.

```bash
# Full pipelines
mind                         # same as: mind --sam3
mind --sam3                  # RealSense + FastFoundation + SAM3 + FlowPose + SigLIP
mind --yolo                  # RealSense + FastFoundation + YOLO + FlowPose + SigLIP

# Basic pipelines
mind --basic-sam3            # RealSense + SAM3 + SigLIP
mind --basic-yolo            # RealSense + YOLO + SigLIP

# Headless / bounded run
mind --sam3 --no-show
mind --basic-yolo --no-show --max-frames 10

# SAM3 prompts
mind --sam3 --sam3-prompts "pen,pencilbag,zipper" --sam3-threshold 0.3

# Help
mind --help
```

## Services

| Service | Port | Conda env | Purpose |
| --- | ---: | --- | --- |
| RealSense | 8000 | `realsense` | RGB, depth, left/right IR capture |
| YOLO | 8001 | `yolo` | Object detection / instance segmentation |
| SigLIP | 8002 | `siglip` | Scene and state classification |
| FastFoundation | 8004 | `fastfoundation` | Stereo depth from IR frames |
| SAM3 | 8005 | `sam3` | Prompt-driven detection / segmentation |
| FlowPose | 8006 | `flowpose` | 6D pose estimation |

Manage services directly:

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

Logs are written to `logs/*.log`; PID files are stored in `/tmp/mindbridge`.

## API

Each service exposes:

```text
GET /health
GET /docs
```

Main inference endpoints:

| Service | Endpoint |
| --- | --- |
| RealSense | `POST /realsense/capture/raw` |
| YOLO | `POST /infer/predict/raw` |
| SigLIP | `POST /infer/predict/raw` |
| FastFoundation | `POST /infer/stereo/raw` |
| SAM3 | `POST /infer/detect/raw` |
| FlowPose | `POST /infer/pose/raw` |

Base64-compatible endpoints also exist for RealSense, YOLO, FastFoundation, and
SAM3. Prefer raw endpoints for runtime performance.

## Project Layout

```text
.
├── build.sh                    # Builds Docker image and installs mindtest
├── Dockerfile                  # CUDA + Miniconda runtime
├── bin/mind                    # Container pipeline launcher
├── scripts/
│   ├── build_env.sh            # Builds Conda environments
│   └── start_service.sh        # Starts/stops FastAPI services
├── mindbridge/
│   ├── src/main.py             # Control Center loop
│   ├── src/MindBridgeClient.py # Service client
│   └── src/core/               # config, launch, controller, service, schemas, tools
└── logs/                       # Service logs
```

## Updating

Code is mounted into the container at `/workspace`, so normal code updates do
not require rebuilding the Docker image. Restart services instead:

```bash
bash scripts/start_service.sh stop
bash scripts/start_service.sh all
```

Re-run `bash build.sh` only when the Docker image or host `mindtest` command
needs to be recreated. Re-run `bash scripts/build_env.sh all` when Conda
environments are missing or dependency definitions changed.
