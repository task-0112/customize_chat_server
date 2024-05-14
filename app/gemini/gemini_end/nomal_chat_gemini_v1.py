"""
gemini通常回答のエンドポイント
"""

# routes/gemini_router.py
from fastapi import APIRouter, WebSocket
from app.gemini.gemini_answer.nomal_chat_gemini_answer import GeminiNomalStreemResponse

router = APIRouter()


@router.websocket("/ws/nomal/chat/gemini/v1")
async def websocket_endpoint(websocket: WebSocket):
    gemini_stream_response = GeminiNomalStreemResponse(websocket)
    await gemini_stream_response.handle_websocket()
