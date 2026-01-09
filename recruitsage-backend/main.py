from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any
import asyncio
from dotenv import load_dotenv

load_dotenv()

# In-memory storage (production: Redis/Memcached)
jobs_db: Dict[str, Dict] = {}
next_job_id = 0

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - no DB connection needed
    print("🚀 RecruitSage API starting (OFFLINE MODE)")
    yield
    print("🛑 API shutdown")

app = FastAPI(title="RecruitSage API", lifespan=lifespan)

# Mock DB session dependency
class MockSession:
    async def execute(self, query, params=None):
        pass
    async def commit(self):
        pass
    async def rollback(self):
        pass

async def get_db():
    yield MockSession()

app.state.jobs_db = jobs_db
app.state.next_job_id = next_job_id
app.state.get_db = get_db

# CORS
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.routes import auth, jobs, resumes, rank
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
app.include_router(rank.router, prefix="/rank", tags=["rank"])

@app.get("/health")
async def health():
    return {"status": "ok", "mode": "OFFLINE", "jobs_count": len(jobs_db)}
