from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Job(BaseModel):
    id: str
    title: str
    location: str
    description: str
    status: str = "Open"

_FAKE_JOBS: List[Job] = [
    Job(id="J-1021", title="Frontend Engineer", location="Remote", description="React/Next.js"),
    Job(id="J-1018", title="Data Analyst", location="Mumbai", description="SQL/Python/Tableau", status="Screening"),
]

@router.get("")
def list_jobs():
    return _FAKE_JOBS

@router.post("")
def create_job(job: Job):
    _FAKE_JOBS.append(job)
    return {"message": "created", "job": job}
