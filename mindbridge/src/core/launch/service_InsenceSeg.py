"""YOLO 推理服务入口（端口 8001）。"""

import sys
import os
sys.path.insert(0, "/workspace")

import uvicorn
from fastapi import FastAPI
from mindbridge.src.core.controller.InstanceSegController import infer_router, init_engine

app = FastAPI(title="YOLO Inference Service")
app.include_router(infer_router)


@app.on_event("startup")
def startup():
    config_path = os.environ.get(
        "YOLO_CONFIG",
        "/workspace/mindbridge/src/core/config/yolo-config.yaml",
    )
    print(f"Loading YOLO model from config: {config_path}")
    init_engine(config_path)
    print("YOLO model loaded, service ready")


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)
