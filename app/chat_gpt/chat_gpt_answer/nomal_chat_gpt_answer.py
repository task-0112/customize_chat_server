"""
ChatGpt選択時の通常回答
"""

from app.settings.env import Env
from app.models.category import GPTType
import openai

# OpenAI APIキーを設定
openai.api_key = Env.OPENAI_API_KEY


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
