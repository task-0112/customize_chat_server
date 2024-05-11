"""
FastAPIアプリケーションにルーティングを設定するモジュール
このモジュールでは、FastAPIアプリケーションにルーターをインクルードし、
エンドポイントをマウントします。
"""

from fastapi import FastAPI
from app.chat_gpt.chat_gpt_end import nomal_chat_gpt_v1
from app.gemini.gemini_end import nomal_chat_gemini_v1


def init_route(app: FastAPI) -> None:
    """
    FastAPIアプリケーションにルーターをインクルードする関数
    """

    # ChatGPTの通常回答
    app.include_router(nomal_chat_gpt_v1.router)

    # Geminiの通常回答
    app.include_router(nomal_chat_gemini_v1.router)
