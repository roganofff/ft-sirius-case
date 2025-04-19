from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer, util
import torch

from requests_api.src.app.models.schemas import MatchResponse

router = APIRouter(
    prefix="/api/requests",
    tags=["Similarity"]
)

model = SentenceTransformer("cointegrated/rubert-tiny2")

base_qa_pairs: List[tuple[str, str]] = []
base_embeddings = []

class BaseQuestion(BaseModel):
    question: str
    answer: str




class MatchRequest(BaseModel):
    description: str

class MatchResult(BaseModel):
    question: str
    score: float

@router.post("/base", status_code=201)
async def add_base_question(q: BaseQuestion):
    try:
        base_qa_pairs.append((q.question, q.answer))
        emb = model.encode(q.question, convert_to_tensor=True)
        base_embeddings.append(emb)
        return {"message": "Base question-answer pair added."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class MatchResult(BaseModel):
    answer: str
    score: float

@router.post("/match", response_model=List[MatchResult])
async def match_question(req: MatchRequest):
    try:
        if not base_qa_pairs:
            raise HTTPException(status_code=400, detail="Base Q&A list is empty.")
        query_emb = model.encode(req.description, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(query_emb, torch.stack(base_embeddings))[0]
        top_k = torch.topk(similarities, k=min(3, len(base_qa_pairs)))
        return [
            MatchResult(answer=base_qa_pairs[i][1], score=float(similarities[i]))
            for i in top_k.indices
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.post("/match", response_model=List[MatchResult])
# async def match_question(req: MatchRequest):
#     if not base_questions:
#         raise HTTPException(status_code=400, detail="Base question list is empty.")
#     try:
#         query_emb = model.encode(req.description, convert_to_tensor=True)
#         embeddings_tensor = torch.stack(base_embeddings)
#         similarities = util.pytorch_cos_sim(query_emb, embeddings_tensor)[0]
#         top_k = torch.topk(similarities, k=min(3, len(base_questions)))
#         return [
#             {"question": base_questions[i], "score": float(similarities[i])}
#             for i in top_k.indices
#         ]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
