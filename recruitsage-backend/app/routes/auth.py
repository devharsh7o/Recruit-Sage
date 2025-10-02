# app/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field  # Field imported
from app.user_store import create_user, get_user
from app.auth_utils import hash_password, verify_password, create_access_token

router = APIRouter()

class SignUp(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    # Keep well below 72 UTF-8 bytes to be safe even with multibyte chars
    password: str = Field(min_length=8, max_length=64)
    role: str = Field(min_length=2, max_length=32)

class SignIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

@router.post("/signup")
def signup(payload: SignUp):
    if get_user(payload.email):
        raise HTTPException(status_code=400, detail="User already exists")
    user = {
        "name": payload.name,
        "email": payload.email,
        "password_hash": hash_password(payload.password),
        "role": payload.role,
    }
    create_user(payload.email, user)
    return {"message": "signup ok", "email": payload.email, "role": payload.role}

@router.post("/signin")
def signin(payload: SignIn):
    user = get_user(payload.email)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=user["email"], extra={"role": user["role"]})
    return {"message": "signin ok", "token": token, "email": user["email"], "role": user["role"]}
