"""
gemini通常回答のエンドポイント
"""

from fastapi import APIRouter
from app.gemini.gemini_answer.nomal_chat_gemini_answer import GeminiNomalStreemResponse
from sse_starlette import EventSourceResponse
from app.schemas.chat import ChatRequest

router = APIRouter()


@router.post("/nomal/chat/gemini/v1")
async def ask_stream(request_body: ChatRequest) -> EventSourceResponse:
    role = request_body.role
    content = request_body.content
    model_type = request_body.modelType
    gpt_normal_stream_response = GeminiNomalStreemResponse(model_type)
    return EventSourceResponse(
        gpt_normal_stream_response._generate_response(role, content)
    )
