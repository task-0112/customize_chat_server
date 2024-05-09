"""
ChatGpt通常回答のエンドポイント
"""

from typing import Dict
from fastapi import APIRouter
from pydantic import BaseModel
from app.chat_gpt.chat_gpt_answer.nomal_chat_gpt_answer import generate_response
from sse_starlette import EventSourceResponse

router = APIRouter()


class AskRequest(BaseModel):
    query: str


# @router.post("/nomal/chat/v1")
# async def chat(request_body: Dict):
#     """
#     ChatGpt通常回答のエンドポイント
#     """
#     print("Received request:", request_body)  # リクエストの内容を出力

#     role = request_body.get("role")
#     content = request_body.get("content")

#     print("Role:", role)  # role の値を出力
#     print("Content:", content)  # content の値を出力

#     if role != "user":
#         print("Invalid role. Raising HTTPException.")  # エラーが発生することを出力
#         raise HTTPException(status_code=400, detail="Invalid role")

#     try:
#         print(
#             "Calling generate_response function."
#         )  # generate_response 関数の呼び出しを出力
#         response = generate_response(role, content)
#         print("Generated response:", response)  # 生成されたレスポンスを出力
#         return response

#     except Exception as e:
#         print("Exception occurred:", str(e))  # 例外が発生したことを出力
#         raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/nomal/chat/v1")
async def ask_stream(request_body: Dict) -> EventSourceResponse:
    role = request_body.get("role")
    content = request_body.get("content")
    print("こっちには来てるよね")
    return EventSourceResponse(generate_response(role, content))
