"""Fast-Foundation Stereo 推理服务入口（端口 8004）。"""

import os
import sys

sys.path.insert(0, "/workspace")

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from mindbridge.src.core.controller.FastFoundationController import infer_router, init_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    config_path = os.environ.get(
        "FASTFOUNDATION_CONFIG",
        "/workspace/mindbridge/src/core/config/fastfoundation-config.yaml",
    )
    print(f"Loading Fast-Foundation Stereo model from config: {config_path}")
    init_engine(config_path)
    print("Fast-Foundation Stereo model loaded, service ready")
    yield


app = FastAPI(title="Fast-Foundation Stereo Inference Service", lifespan=lifespan)
app.include_router(infer_router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004, reload=False)
