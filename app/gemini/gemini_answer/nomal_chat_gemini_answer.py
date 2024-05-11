"""
gemini選択時の通常回答
"""

from vertexai.generative_models import GenerativeModel
from app.models.category import GPTType
from app.settings.vertexai_config import init_vertexai, safety_settings


class GeminiNomalStreemResponse:
    def __init__(self, model_type: int):
        self.model_type = model_type
        init_vertexai()

    def get_model_name(self):
        gpt_type = GPTType(self.model_type)
        return gpt_type.get_gpt_model_name()

    async def _generate_response(self, role: str, content: str):
        try:
            model_name = self.get_model_name()
            model = GenerativeModel(
                model_name,
                safety_settings=safety_settings,
                system_instruction=[
                    "出来る限り日本語で会話をしてください",
                ],
            )
            prompt = content
            completion = model.generate_content(
                prompt,
                stream=True,
            )
            buffer = ""
            for chunk in completion:
                print("chunk_message", chunk.text)
                yield {"data": chunk.text}
            if buffer:
                yield {"data": buffer}

        except Exception as e:
            raise e
