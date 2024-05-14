"""
ChatGpt選択時の通常回答
"""

import asyncio
import logging
from fastapi import WebSocket, WebSocketDisconnect
import openai
from app.models.category import GPTType
from app.settings.env import Env

# OpenAI APIキーを設定
openai.api_key = Env.OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)


class GptNomalStreemResponse:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.stop_generating = False

    def get_model_name(self, model_type: int):
        gpt_type = GPTType(model_type)
        return gpt_type.get_gpt_model_name()

    async def handle_websocket(self):
        try:
            await self.websocket.accept()
            while True:
                message = await self.websocket.receive_json()
                if message.get("type") == "stop":
                    self.stop_generating = True
                    break
                else:
                    model_type = message.get("modelType")
                    role = message.get("role")
                    content = message.get("content")
                    await self._generate_streaming_response(model_type, role, content)
        except WebSocketDisconnect:
            logging.info("WebSocket disconnected")
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
        finally:
            self.stop_generating = True
            if self.websocket.application_state == "CONNECTED":
                await self.websocket.close()

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
                    if self.websocket.application_state != "CLOSED":
                        await self.websocket.send_json(
                            {"type": "assistant", "content": buffer}
                        )
                    await asyncio.sleep(0.1)
            if not self.stop_generating:
                if self.websocket.application_state != "CLOSED":
                    await self.websocket.send_json({"type": "end"})
            self.stop_generating = False
        except Exception as e:
            logging.error(f"Error in generating response: {e}")
            if self.websocket.application_state != "CLOSED":
                await self.websocket.close()
