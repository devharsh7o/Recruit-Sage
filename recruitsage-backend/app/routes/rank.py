from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class RankRequest(BaseModel):
    resume_text: str
    job_description: str

@router.post("")
def rank(req: RankRequest) -> Dict[str, float]:
    # Very simple overlap-based mock score (0–100)
    r = set(req.resume_text.lower().split())
    j = set(req.job_description.lower().split())
    if not j:
        return {"score": 0.0}
    overlap = len(r & j)
    score = round((overlap / len(j)) * 100, 2)
    return {"score": score}
