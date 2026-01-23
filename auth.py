from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from database import SessionLocal
from models import User

SECRET_KEY = "CHANGE_ME_NOW"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hash):
    return pwd_context.verify(password, hash)

def create_token(user: User):
    return jwt.encode(
        {"sub": user.username, "role": user.role},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

@router.post("/register")
def register(username: str, password: str, role: str = "viewer", db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(400, "User already exists")

    user = User(
        username=username,
        password_hash=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    return {"status": "user created"}

@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data["username"]).first()
    if not user or not verify_password(data["password"], user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    return {"token": create_token(user), "role": user.role}