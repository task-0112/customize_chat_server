"""
gemini選択時の通常回答
"""

# gemini_answer/nomal_chat_gemini_answer.py
import asyncio
import logging
from fastapi import WebSocket, WebSocketDisconnect
from vertexai.generative_models import GenerativeModel
from app.models.category import GPTType
from app.settings.vertexai_config import init_vertexai, safety_settings


class GeminiNomalStreemResponse:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.stop_generating = False
        init_vertexai()

    def get_model_name(self, model_type: int):
        gpt_type = GPTType(model_type)
        return gpt_type.get_gpt_model_name()

    async def handle_websocket(self):
        await self.websocket.accept()
        try:
            while True:
                message = await self.websocket.receive_json()
                if message.get("type") == "stop":
                    self.stop_generating = True
                    await self.websocket.close()
                    break
                else:
                    model_type = message.get("modelType")
                    role = message.get("role")
                    content = message.get("content")
                    await self._generate_response(model_type, role, content)
        except WebSocketDisconnect:
            logging.info("WebSocket disconnected")
            self.stop_generating = True
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
            try:
                await self.websocket.close()
            except Exception:
                pass

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
                try:
                    await self.websocket.send_json(
                        {"type": "assistant", "content": buffer}
                    )
                    await asyncio.sleep(0.1)
                except WebSocketDisconnect:
                    logging.info("WebSocket disconnected during generation")
                    return
            if not self.stop_generating:
                print("Response generation completed")
                try:
                    await self.websocket.send_json({"type": "end"})
                except WebSocketDisconnect:
                    logging.info("WebSocket disconnected after generation")
            self.stop_generating = False
        except Exception as e:
            raise e
