from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import (
    tests_endpoint,
)
from app.core.config import settings
from app.core.logging import init_logging
from app.settings.route import init_route

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
