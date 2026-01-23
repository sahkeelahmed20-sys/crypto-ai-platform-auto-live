from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import bcrypt, jwt, os
from datetime import datetime, timedelta

from database import get_db
from users import User

router = APIRouter()
SECRET = os.getenv("JWT_SECRET", "supersecretkey")
ALGO = "HS256"

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "user"

def create_token(user: User):
    return jwt.encode(
        {
            "sub": user.username,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(hours=12)
        },
        SECRET,
        algorithm=ALGO
    )

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(400, "User exists")

    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

    user = User(
        username=data.username,
        password=hashed.decode(),
        role=data.role
    )
    db.add(user)
    db.commit()
    return {"status": "created"}

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(401, "Invalid credentials")

    if not bcrypt.checkpw(data.password.encode(), user.password.encode()):
        raise HTTPException(401, "Invalid credentials")

    return {"token": create_token(user)}