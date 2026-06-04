"""FlowPose 6D姿态估计 推理服务入口（端口 8006）。"""

import os
import sys

sys.path.insert(0, "/workspace")

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from mindbridge.src.core.controller.FlowPoseController import infer_router, init_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    config_path = os.environ.get(
        "FLOWPOSE_CONFIG",
        "/workspace/mindbridge/src/core/config/flowpose-config.yaml",
    )
    print(f"Loading FlowPose model from config: {config_path}")
    init_engine(config_path)
    print("FlowPose model loaded, service ready")
    yield


app = FastAPI(title="FlowPose 6D Pose Estimation Service", lifespan=lifespan)
app.include_router(infer_router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006, reload=False)
