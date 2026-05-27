import sys
import os

sys.path.insert(0, "/workspace")

from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from mindbridge.src.core.controller.Controlcenter import control_router
import uvicorn
import logging
from loguru import logger

LOG_PATH = "../logs"
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # 从标准 logging 适配到 loguru
        try:
            level = logger.level(record.levelname).name
        except Exception:
            level = record.levelno

        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())

def setup_logging():
    logger.remove()

    logger.add(sys.stdout,
               level="DEBUG",
               colorize=True,
               format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                      "<level>{level: <8}</level> | "
                      "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                      "<level>{message}</level>")

    logger.add(f"{LOG_PATH}/app_{{time:YYYY-MM-DD}}.log",
               rotation="100 MB",
               retention="15 days",
               compression="zip",
               encoding="utf-8",
               level="INFO")

    # 将 uvicorn 与 logging 框架输出交给 loguru
    logging.root.handlers = [InterceptHandler()]    # ★ 只设置一次 handler
    logging.root.setLevel(logging.INFO)

    # 清空 uvicorn 子 logger，自然会冒泡到 root logger
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True     # ★ 让日志冒泡即可

    class StreamToLogger(object):
        def write(self, message):
            if message.strip():
                logger.info(message.strip())

        def flush(self): pass
        def isatty(self): return False

    sys.stdout = StreamToLogger()
    sys.stderr = StreamToLogger()


setup_logging()
logger.info("日志系统初始化完成")


app = FastAPI()

app.include_router(control_router)



origins = [
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,         
    allow_methods=["*"],            
    allow_headers=["*"],            
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    logger.info("Starting MindBridge ...")
    uvicorn.run(app, host="0.0.0.0", port=6666,
                log_config=None,     
                access_log=False
                )