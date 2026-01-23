from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

router = APIRouter()

SECRET = os.getenv("JWT_SECRET", "supersecretkey")
ALGO = "HS256"

# demo admin user
ADMIN_USER = {
    "username": "admin",
    "password": bcrypt.hashpw(b"admin123", bcrypt.gensalt())
}

class LoginRequest(BaseModel):
    username: str
    password: str

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)

@router.post("/login")
def login(data: LoginRequest):
    if data.username != ADMIN_USER["username"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not bcrypt.checkpw(data.password.encode(), ADMIN_USER["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"token": create_token(data.username)}