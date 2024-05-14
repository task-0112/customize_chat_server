"""
ChatGpt選択時の通常回答
"""

import logging
from fastapi import WebSocket
import openai
from app.models.category import GPTType
from app.settings.env import Env
from app.schemas.streaming_response import BaseStreamingResponse

# OpenAI APIキーを設定
openai.api_key = Env.OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)


class GptNomalStreemResponse(BaseStreamingResponse):
    def __init__(self, websocket: WebSocket):
        super().__init__(websocket)

    def get_model_name(self, model_type: int):
        gpt_type = GPTType(model_type)
        return gpt_type.get_gpt_model_name()

    async def handle_websocket(self):
        await super().handle_websocket(self._generate_streaming_response)

    async def _generate_streaming_response(
        self, model_type: int, role: str, content: str
    ):
        try:
            model_name = self.get_model_name(model_type)
            response = await openai.ChatCompletion.acreate(
                model=model_name,
                messages=[{"role": role, "content": content}],
                stream=True,
            )
            buffer = ""
            async for chunk in response:
                chunk_message = chunk["choices"][0]["delta"].get("content", "")
                if chunk_message:
                    buffer += chunk_message
                    await self.send_response_chunk(buffer)
            if not self.stop_generating:
                await self.end_response()
            self.stop_generating = False
        except Exception as e:
            logging.error(f"Error in generating response: {e}")
            if self.websocket.application_state != "CLOSED":
                await self.websocket.close()
