"""
ChatGpt選択時の回答
"""

import os
import openai

# OpenAI APIキーを設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


async def generate_response(role: str, content: str):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
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
