from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Path as FPath
from typing import Optional
from pathlib import Path as SysPath
import time
import uuid

from app.store import save_resume, get_resume
from app.utils_extract import extract_text

router = APIRouter()

UPLOAD_DIR = SysPath(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
MAX_SIZE_MB = 10


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_id: Optional[str] = Form(None),
    candidate_name: Optional[str] = Form(None),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await file.read()
    size_kb = round(len(content) / 1024, 2)
    if len(content) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large (> {MAX_SIZE_MB} MB)")

    safe_name = file.filename.replace("/", "_").replace("\\", "_")
    unique_name = f"{int(time.time() * 1000)}__{safe_name}"
    dest_path = UPLOAD_DIR / unique_name

    with open(dest_path, "wb") as f:
        f.write(content)
    del content

    text = extract_text(dest_path, file.content_type)
    resume_id = str(uuid.uuid4())
    save_resume(resume_id, {
        "resume_id": resume_id,
        "original_filename": file.filename,
        "stored_as": unique_name,
        "stored_path": str(dest_path),
        "content_type": file.content_type,
        "size_kb": size_kb,
        "job_id": job_id,
        "candidate_name": candidate_name,
        "extracted_text": text,
        "created_at": int(time.time()),
    })

    return {
        "resume_id": resume_id,
        "filename": file.filename,
        "stored_as": unique_name,
        "size_kb": size_kb,
        "status": "stored",
        "extracted_preview_chars": len(text[:200]),
    }


@router.get("/{resume_id}")
def get_resume_detail(resume_id: str = FPath(..., description="Resume ID from the upload response")):
    data = get_resume(resume_id)
    if not data:
        raise HTTPException(status_code=404, detail="Resume not found")

    preview_len = 5000
    preview_text = (data.get("extracted_text") or "")[:preview_len]

    return {
        **data,
        "extracted_text": preview_text,
        "preview_len": len(preview_text),
        "note": f"Preview limited to {preview_len} characters",
    }
