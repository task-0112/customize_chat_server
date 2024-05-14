from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import (
    tests_endpoint,
)

from app.core.config import settings
from app.core.logging import init_logging
from app.settings.route import init_route

import uvicorn

import logging
from logging.handlers import RotatingFileHandler
import sys


def init_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # 最低レベルをDEBUGに設定
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),  # 標準出力へのハンドラー
            RotatingFileHandler(
                filename="app.log", maxBytes=10000, backupCount=3
            ),  # ファイル出力のハンドラー
        ],
    )


app = FastAPI()
init_logging()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # フロントエンドのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

app.include_router(tests_endpoint.router, prefix="/api/v1", tags=["tests"])
init_route(app)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, log_level="debug")
