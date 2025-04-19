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

base_questions: List[str] = []
base_embeddings = []

class BaseQuestion(BaseModel):
    text: str

class MatchRequest(BaseModel):
    description: str

class MatchResult(BaseModel):
    question: str
    score: float

@router.post("/base", status_code=201)
async def add_base_question(q: BaseQuestion):
    try:
        base_questions.append(q.text)
        emb = model.encode(q.text, convert_to_tensor=True)
        base_embeddings.append(emb)
        return {"message": "Base question added."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/match", response_model=List[MatchResponse])
async def match_question(req: MatchRequest):
   if not base_questions:
       raise HTTPException(status_code=400, detail="Base question list is empty.")
   try:
       query_emb = model.encode(req.description, convert_to_tensor=True)
       embeddings_tensor = torch.stack(base_embeddings)
       similarities = util.pytorch_cos_sim(query_emb, embeddings_tensor)[0]
       top_k = torch.topk(similarities, k=min(3, len(base_questions)))
       return [
           MatchResponse(question=base_questions[i], score=float(similarities[i]))
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
