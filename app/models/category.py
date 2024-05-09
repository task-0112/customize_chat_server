from enum import Enum


class GPTType(Enum):
    GPT35Turbo = 0
    GPT4 = 1
    GeminiPro = 2
    Claude3Opus = 3
    Claude3Sonnet = 4
    Claude3Haiku = 5

    def get_gpt_model_name(self):
        if self == GPTType.GPT35Turbo:
            return "gpt-3.5-turbo-0125"
        elif self == GPTType.GPT4:
            return "gpt-4-turbo-2024-04-09"
