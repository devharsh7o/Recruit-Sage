from sqlalchemy import Column, String, Text, ARRAY, Numeric, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    company = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(ARRAY(String), default=list)
    created_by = Column(String, nullable=False)  # HR email
    status = Column(String, default="Open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    candidate_email = Column(String, nullable=False)
    resume = Column(String, nullable=False)  # filename/path
    score = Column(Numeric(5,2))
    explanation = Column(Text)  # JSON string
    status = Column(String, default="Applied")
    applied_at = Column(DateTime(timezone=True), server_default=func.now())

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_email = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    size_kb = Column(String)
    extracted_text = Column(Text)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
