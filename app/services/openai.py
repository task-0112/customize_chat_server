import os
import openai


class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def create_chat_completion(self, model_name, messages, stream=False):
        return openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            stream=stream,
        )
