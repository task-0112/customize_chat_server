from pydantic import BaseModel


class ChatRequest(BaseModel):
    role: str
    content: str
    modelType: int


class ChatResponse(BaseModel):
    data: str
