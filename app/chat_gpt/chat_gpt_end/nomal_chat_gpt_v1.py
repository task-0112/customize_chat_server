"""
ChatGpt通常回答のエンドポイント
"""

from typing import Dict
from fastapi import APIRouter
from pydantic import BaseModel
from app.chat_gpt.chat_gpt_answer.nomal_chat_gpt_answer import GptNomalStreemResponse
from sse_starlette import EventSourceResponse

router = APIRouter()


class AskRequest(BaseModel):
    query: str


@router.post("/nomal/chat/v1")
async def ask_stream(request_body: Dict) -> EventSourceResponse:
    role = request_body.get("role")
    content = request_body.get("content")
    model_type = request_body.get("modelType")
    gpt_normal_stream_response = GptNomalStreemResponse(model_type)
    return EventSourceResponse(
        gpt_normal_stream_response._generate_response(role, content)
    )
