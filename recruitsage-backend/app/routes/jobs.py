from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
from app.models import JobCreate  # Your Pydantic model for job input
from app.role_deps import require_role, get_current_user
from uuid import uuid4

router = APIRouter()
jobs_store = {}
applications_store = {}  # key: job_id, value: list of applications

@router.post("/jobs", response_model=dict)
def create_job(job: JobCreate, user=Depends(require_role("HR"))):
    job_id = str(uuid4())
    jobs_store[job_id] = {
        "id": job_id,
        "title": job.title,
        "company": job.company if hasattr(job, "company") else None,
        "location": job.location,
        "description": job.description,
        "tags": job.tags if hasattr(job, "tags") else [],
        "created_by": user["sub"],  # User email from JWT payload
        "status": "Open"
    }
    return {"message": "Job created", "job": jobs_store[job_id]}

@router.get("/jobs", response_model=List[dict])
def list_jobs():
    return list(jobs_store.values())

@router.patch("/jobs/{job_id}", response_model=dict)
def update_job(job_id: str, job_update: JobCreate, user=Depends(require_role("HR"))):
    job = jobs_store.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if job["created_by"] != user["sub"]:
        raise HTTPException(403, "Forbidden to edit this job")
    updated_data = job_update.dict(exclude_unset=True)
    for k, v in updated_data.items():
        job[k] = v
    jobs_store[job_id] = job
    return job

@router.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: str, user=Depends(require_role("HR"))):
    job = jobs_store.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if job["created_by"] != user["sub"]:
        raise HTTPException(403, "Forbidden to delete this job")
    del jobs_store[job_id]

# ---------- Candidate Application Endpoints ----------

@router.post("/jobs/{job_id}/apply", response_model=dict)
def apply_to_job(job_id: str, resume: str = Body(...), user=Depends(require_role("candidate"))):
    app = {"candidate": user["sub"], "resume": resume, "status": "Applied"}
    applications_store.setdefault(job_id, []).append(app)
    return {"message": "Application submitted", "application": app}

@router.get("/jobs/{job_id}/applications", response_model=list)
def list_applications(job_id: str, user=Depends(require_role("HR"))):
    return applications_store.get(job_id, [])
