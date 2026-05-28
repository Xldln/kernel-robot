"""YOLO 推理服务入口（端口 8001）。"""

import sys
import os
sys.path.insert(0, "/workspace")

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from mindbridge.src.core.controller.InstanceSegController import infer_router, init_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    config_path = os.environ.get(
        "YOLO_CONFIG",
        "/workspace/mindbridge/src/core/config/yolo-config.yaml",
    )
    print(f"Loading YOLO model from config: {config_path}")
    init_engine(config_path)
    print("YOLO model loaded, service ready")
    yield


app = FastAPI(title="YOLO Inference Service", lifespan=lifespan)
app.include_router(infer_router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)
