"""
ChatGpt通常回答のエンドポイント
"""

from fastapi import APIRouter, WebSocket
from app.chat_gpt.chat_gpt_answer.nomal_chat_gpt_answer import GptNomalStreemResponse

router = APIRouter()


@router.websocket("/ws/nomal/chat/gpt/v1")
async def websocket_endpoint(websocket: WebSocket):
    gpt_stream_response = GptNomalStreemResponse(websocket)
    await gpt_stream_response.handle_websocket()
