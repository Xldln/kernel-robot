"""RealSense 深度服务入口（端口 8000）。"""

import sys
import os
sys.path.insert(0, "/workspace")

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from mindbridge.src.core.controller.RealSenseController import (
    realsense_router,
    init_engine,
    close_engine,
    engine_status,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    config_path = os.environ.get(
        "REALSENSE_CONFIG",
        "/workspace/mindbridge/src/core/config/realsense-config.yaml",
    )
    print(f"Loading RealSense from config: {config_path}")
    init_engine(config_path)
    print("RealSense service ready")
    try:
        yield
    finally:
        print("RealSense service shutting down")
        close_engine()


app = FastAPI(title="RealSense Depth Service", lifespan=lifespan)
app.include_router(realsense_router)


@app.get("/health")
def health():
    return engine_status()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
