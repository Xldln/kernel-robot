"""SAM3 目标检测 / 分割 推理服务入口（端口 8005）。"""

import os
import sys

sys.path.insert(0, "/workspace")

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from mindbridge.src.core.controller.Sam3Controller import infer_router, init_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    config_path = os.environ.get(
        "SAM3_CONFIG",
        "/workspace/mindbridge/src/core/config/sam3-config.yaml",
    )
    print(f"Loading SAM3 model from config: {config_path}")
    init_engine(config_path)
    print("SAM3 model loaded, service ready")
    yield


app = FastAPI(title="SAM3 Inference Service", lifespan=lifespan)
app.include_router(infer_router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005, reload=False)
