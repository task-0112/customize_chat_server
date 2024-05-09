"""
FastAPIアプリケーションにルーティングを設定するモジュール
このモジュールでは、FastAPIアプリケーションにルーターをインクルードし、
エンドポイントをマウントします。
"""
from fastapi import FastAPI
from app.chat_gpt.chat_gpt_end import nomal_chat_gpt_v1

def init_route(app: FastAPI) -> None:
    """
    FastAPIアプリケーションにルーターをインクルードする関数
    """
    app.include_router(nomal_chat_gpt_v1.router)
