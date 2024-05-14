"""
gemini選択時の通常回答
"""

import logging
from fastapi import WebSocket
from vertexai.generative_models import GenerativeModel
from app.models.category import GPTType
from app.settings.vertexai_config import init_vertexai, safety_settings
from app.schemas.streaming_response import BaseStreamingResponse

logging.basicConfig(level=logging.INFO)


class GeminiNomalStreemResponse(BaseStreamingResponse):
    def __init__(self, websocket: WebSocket):
        super().__init__(websocket)
        init_vertexai()

    def get_model_name(self, model_type: int):
        gpt_type = GPTType(model_type)
        return gpt_type.get_gpt_model_name()

    async def handle_websocket(self):
        await super().handle_websocket(self._generate_response)

    async def _generate_response(self, model_type: int, role: str, content: str):
        try:
            model_name = self.get_model_name(model_type)
            model = GenerativeModel(
                model_name,
                safety_settings=safety_settings,
                system_instruction=["出来る限り日本語で会話をしてください"],
            )
            prompt = content
            completion = model.generate_content(prompt, stream=True)
            buffer = ""
            for chunk in completion:
                if self.stop_generating:
                    break
                buffer += chunk.text
                await self.send_response_chunk(buffer)
            if not self.stop_generating:
                await self.end_response()
            self.stop_generating = False
        except Exception as e:
            logging.error(f"Error in generating response: {e}")
            if self.websocket.application_state != "CLOSED":
                await self.websocket.close()
