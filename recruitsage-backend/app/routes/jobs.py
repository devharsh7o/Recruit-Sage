from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import uuid4
from app.role_deps import require_role, get_current_user
from main import get_db
from app.models import Job, Application

router = APIRouter()

# In-memory jobs storage (shared with main.py)
jobs_db = []

@router.post("/", response_model=dict)
async def create_job(
    job_data: dict, 
    user=Depends(require_role("HR")), 
    db=Depends(get_db)
):
    job_id = str(uuid4())
    job = {
        **job_data,
        "id": job_id,
        "created_by": user["sub"],
        "status": "Open",
        "created_at": "2026-01-09T10:00:00Z"
    }
    
    jobs_db.append(job)
    print(f"✅ Job created: ID={job_id} by {user['sub']} (OFFLINE)")
    
    return {
        "message": "Job created successfully ✅ (OFFLINE MODE)", 
        "job_id": job_id,
        "job": job
    }

@router.get("/", response_model=List[dict])
async def list_jobs(db=Depends(get_db)):
    print(f"📋 Listing {len(jobs_db)} jobs (OFFLINE)")
    return jobs_db

@router.patch("/{job_id}", response_model=dict)
async def update_job(
    job_id: str, 
    job_update: dict, 
    user=Depends(require_role("HR")), 
    db=Depends(get_db)
):
    for job in jobs_db:
        if job["id"] == job_id:
            if job["created_by"] != user["sub"]:
                raise HTTPException(403, "You can only edit your own jobs")
            
            for key, value in job_update.items():
                job[key] = value
            
            print(f"✅ Job updated: ID={job_id} (OFFLINE)")
            return {"message": "Job updated successfully ✅ (OFFLINE)", "job_id": job_id}
    
    raise HTTPException(404, "Job not found")

@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: str, user=Depends(require_role("HR")), db=Depends(get_db)):
    global jobs_db
    initial_count = len(jobs_db)
    jobs_db = [job for job in jobs_db if not (job["id"] == job_id and job["created_by"] != user["sub"])]
    
    if len(jobs_db) == initial_count:
        raise HTTPException(404, "Job not found or not authorized")
    
    print(f"✅ Job deleted: ID={job_id} (OFFLINE)")
    return None


# Applications (mock)
applications_db = {}

@router.post("/{job_id}/apply", response_model=dict)
async def apply_to_job(
    job_id: str, 
    resume: str = Body(..., embed=True), 
    user=Depends(require_role("candidate")), 
    db=Depends(get_db)
):
    app_id = str(uuid4())
    applications_db[app_id] = {
        "id": app_id,
        "job_id": job_id,
        "candidate_email": user["sub"],
        "resume": resume,
        "status": "Applied"
    }
    print(f"✅ Application submitted: {app_id} (OFFLINE)")
    return {"message": "Application submitted ✅ (OFFLINE)", "application": applications_db[app_id]}

@router.get("/{job_id}/applications", response_model=List[dict])
async def list_applications(job_id: str, user=Depends(require_role("HR")), db=Depends(get_db)):
    apps = [app for app in applications_db.values() if app["job_id"] == job_id]
    print(f"📋 {len(apps)} applications for job {job_id} (OFFLINE)")
    return apps
