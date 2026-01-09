from pydantic import BaseModel, Field
from typing import List, Optional

class JobCreate(BaseModel):
    title: str = Field(..., max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    tags: Optional[List[str]] = []

# Add these response models too
class JobResponse(BaseModel):
    id: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    created_by: str
    status: str
    created_at: str
    
    class Config:
        from_attributes = True  # For SQLAlchemy compatibility
