from pydantic import BaseModel
from datetime import datetime

class RequestCreate(BaseModel):
    user_id: int
    description: str

class RequestOut(RequestCreate):
    id: str
    created_at: datetime
    updated_at: datetime