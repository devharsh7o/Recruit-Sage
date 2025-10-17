from pydantic import BaseModel, Field
from typing import List, Optional

class JobCreate(BaseModel):
    title: str = Field(..., max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    tags: Optional[List[str]] = []

