"""
ChatGpt選択時の回答
"""

import os
import openai
from app.models.category import GPTType

# OpenAI APIキーを設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


class GptNomalStreemResponse:
    def __init__(self, model_type: int):
        self.model_type = model_type

    def get_model_name(self):
        gpt_type = GPTType(self.model_type)
        return gpt_type.get_gpt_model_name()

    async def _generate_response(self, role: str, content: str):
        try:
            model_name = self.get_model_name()
            completion = openai.ChatCompletion.create(
                model=model_name,
                messages=[{"role": role, "content": content}],
                stream=True,
            )
            buffer = ""
            for chunk in completion:
                chunk_message = chunk["choices"][0]["delta"].get("content", "")
                print("chunk_message", chunk_message)
                yield {"data": chunk_message}
            if buffer:
                yield {"data": buffer}

        except Exception as e:
            raise e
