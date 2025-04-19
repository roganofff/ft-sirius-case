from pydantic import BaseModel


class SelectionRequest(BaseModel):
    question: str
    candidates: list[str]


class SelectionResponse(BaseModel):
    chosen: str
    index: int
