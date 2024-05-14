import asyncio
import logging
from fastapi import WebSocket, WebSocketDisconnect

logging.basicConfig(level=logging.INFO)


class BaseStreamingResponse:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.stop_generating = False

    async def handle_websocket(self, generate_response_func):
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
                    await generate_response_func(model_type, role, content)
        except WebSocketDisconnect:
            logging.info("WebSocket disconnected")
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
        finally:
            self.stop_generating = True
            if self.websocket.application_state == "CONNECTED":
                await self.websocket.close()

    async def send_response_chunk(self, buffer: str):
        if self.websocket.application_state != "CLOSED":
            await self.websocket.send_json({"type": "assistant", "content": buffer})
            await asyncio.sleep(0.1)

    async def end_response(self):
        if self.websocket.application_state != "CLOSED":
            await self.websocket.send_json({"type": "end"})
