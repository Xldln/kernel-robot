# MindBridge / TJfusion

MindBridge is a local inference pipeline for RealSense + vision models + robot execution. The recommended deployment: **one main image `tjfusion:latest`, one main container `TJfusion`**, running all MindBridge services inside.

## Architecture

```text
TJfusion container
├── Fusion Web UI              :8765
├── RealSense service          :8000
├── YOLO service               :8001
├── SigLIP service             :8002
├── FastFoundation service     :8004
├── SAM3 service               :8005
└── FlowPose service           :8006
```

Service logs:

```text
logs/*.log
```

Service PIDs inside the container:

```text
/tmp/mindbridge/*.pid
```

## Quick Start

From the repo root:

```bash
./run.sh
```

Open:

```text
http://127.0.0.1:8765
```

`./run.sh` starts or reuses the `TJfusion` container and launches Fusion Web UI inside it.

## Enter the Container

```bash
tjfusion
```

Equivalent to:

```bash
docker exec -it TJfusion bash
```

If `tjfusion` is not found, make sure `~/.local/bin` is in your `PATH`:

```bash
echo "$PATH"
```

## Pipelines

Run inside the `TJfusion` container.

```bash
mind
```

Starts the default full SAM3 pipeline:

```text
RealSense + FastFoundation + SAM3 + FlowPose + SigLIP
```

Full YOLO pipeline:

```bash
mind --yolo
```

Basic pipelines (no FastFoundation + FlowPose):

```bash
mind --basic-sam3
mind --basic-yolo
```

Standalone modes:

```bash
mind --yolo-only
mind --sam3-only
mind --siglip-only
mind --flowpose-only
mind --rs-only
```

Headless mode:

```bash
mind --yolo --no-show
```

### Extra Arguments

All pipeline commands accept additional arguments:

```bash
mind --show                         # show OpenCV windows (default)
mind --no-show                      # headless, no display
mind --rgb-source usb               # use USB webcam instead of RealSense
mind --fusion-pub                   # publish Fusion ZMQ results to :8899
mind --fusion-ui-url http://127.0.0.1:8765  # push video frames to Fusion UI
```

## Multi-Camera Mode

When multiple RealSense cameras are connected (1 primary + N aux color-only cameras), use `--camera-mode multi`:

```bash
mind --camera-mode multi
```

In this mode:
- **Primary camera**: full capture (color + depth + IR) — used for detection, depth estimation, and pose estimation
- **Aux cameras**: color-only frames — used to enrich SigLIP multi-view state classification
- **SigLIP**: all camera views are horizontally stitched into a single multi-view image for joint classification, improving accuracy
- **Visualization**: an additional `SigLIP MultiView` window shows the stitched multi-view feed

Single camera mode (default):

```bash
mind --camera-mode single
```

Note: `multi` mode only works with `--rgb-source realsense` (the default). USB cameras do not support multi-camera mode.

## Service Management

Inside the `TJfusion` container:

```bash
bash scripts/start_service.sh status
bash scripts/start_service.sh yolo-full          # YOLO full pipeline dependencies
bash scripts/start_service.sh sam3-full          # SAM3 full pipeline dependencies
bash scripts/start_service.sh basic-yolo         # YOLO basic pipeline dependencies
bash scripts/start_service.sh basic-sam3         # SAM3 basic pipeline dependencies
bash scripts/start_service.sh flowpose-stack     # FlowPose pipeline dependencies
bash scripts/start_service.sh all                # all services
bash scripts/start_service.sh stop               # stop all
bash scripts/start_service.sh restart            # restart all
```

Start individual services:

```bash
bash scripts/start_service.sh realsense
bash scripts/start_service.sh yolo
bash scripts/start_service.sh sam3
bash scripts/start_service.sh siglip
bash scripts/start_service.sh fastfoundation
bash scripts/start_service.sh flowpose
```

## RealSense Health Check

RealSense requires both `/health` and the camera engine to be healthy:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/realsense/info
```

A healthy `/realsense/info` returns camera intrinsics.  
If you see `engine_missing` or `Engine not initialized`, restart the RealSense service:

```bash
bash scripts/start_service.sh realsense
```

## FlowPose Visualization

The FlowPose visualization window size is configured in:

```text
mindbridge/src/core/config/flowpose-config.yaml
```

When the window is focused, press `ESC` or `q` to close the visualization window (the FlowPose service keeps running).

Toggle visualization via API:

```bash
# disable
curl -X POST 'http://127.0.0.1:8006/infer/visualization?enabled=false'
# enable
curl -X POST 'http://127.0.0.1:8006/infer/visualization?enabled=true'
```

## Docker Notes

List running containers:

```bash
docker ps
```

You should see:

```text
TJfusion
```

`TJfusion` is the container name, not the image name.  
`docker images` shows images, e.g.:

```text
tjfusion:latest
```

If `docker ps` shows `TJfusion`'s IMAGE as an image ID (e.g. `f759...`), the container was created using the image ID. Functionality is unaffected. To have it display `tjfusion:latest`, recreate the container (no need to delete the image).

## Updating Code

The repo is mounted at `/workspace` inside the container. Code changes usually do not require an image rebuild — just restart the relevant services:

```bash
bash scripts/start_service.sh stop
bash scripts/start_service.sh yolo-full
```

Only rebuild the image or re-create the conda environment when image dependencies, conda environments, or system packages change.
