from fastapi import Depends, HTTPException, status
from app.auth_utils import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_token(token.credentials)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def require_role(role: str):
    def role_checker(user=Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker
