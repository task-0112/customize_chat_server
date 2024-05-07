from functools import lru_cache

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(), override=True)


class Settings(BaseSettings):
    # アプリケーションの設定値
    PROJECT_NAME: str
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # フロントエンドのURL
    FRONTEND_URL: str = "http://localhost:3001"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
