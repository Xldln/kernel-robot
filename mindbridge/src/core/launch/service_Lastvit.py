"""LAST-ViT 推理服务入口（端口 8002）。"""

import os
import sys
sys.path.insert(0, "/workspace")

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from mindbridge.src.core.controller.LastvitController import infer_router, init_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    config_path = os.environ.get(
        "LASTVIT_CONFIG",
        "/workspace/mindbridge/src/core/config/last-vit-config.yaml",
    )
    print(f"Loading LAST-ViT model from config: {config_path}")
    init_engine(config_path)
    print("LAST-ViT model loaded, service ready")
    yield


app = FastAPI(title="LAST-ViT Inference Service", lifespan=lifespan)
app.include_router(infer_router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=False)
