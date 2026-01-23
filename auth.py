from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import bcrypt
import jwt
import os

router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGO = "HS256"

# ✅ DEMO USER (PLAIN PASSWORD)
USERS = {
    "admin": bcrypt.hashpw(b"admin123", bcrypt.gensalt())
}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    user = USERS.get(data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ HASH ONLY THE USER PASSWORD
    if not bcrypt.checkpw(data.password.encode(), user):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": data.username}, JWT_SECRET, algorithm=JWT_ALGO)

    return {"token": token}