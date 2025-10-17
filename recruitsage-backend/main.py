from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import jobs
from app.routes import auth, jobs, resumes, rank
import os


load_dotenv()

app = FastAPI(title="RecruitSage API")

# CORS
origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from app.routes import auth, jobs, resumes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
app.include_router(rank.router, prefix="/rank", tags=["rank"])

app.include_router(jobs.router)

@app.get("/health")
def health():
    return {"status": "ok"}
