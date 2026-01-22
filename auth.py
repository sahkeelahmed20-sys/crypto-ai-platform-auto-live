from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ⚠️ HASH ONCE (hardcoded for now)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = pwd_context.hash("admin123")


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest):
    if data.username != ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ VERIFY — NOT hash again
    if not pwd_context.verify(data.password, ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": "demo-token-admin",
        "token_type": "bearer"
    }