from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    success: bool


class SelectionRequest(BaseModel):
    question: str
    candidates: list[str]


class SelectionResponse(BaseModel):
    chosen: str
    index: int
