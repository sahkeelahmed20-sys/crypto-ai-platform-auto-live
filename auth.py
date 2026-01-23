from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from database import SessionLocal
from models import User

security = HTTPBearer()

SECRET_KEY = "CHANGE_ME_NOW"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
        
def require_role(*allowed_roles):
    def checker(user=Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return checker

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
    
@router.get("/admin/only")
def admin_only(user=Depends(require_role("admin"))):
    return {
        "message": "Welcome Admin",
        "user": user["sub"]
    }
    
@router.get("/trade/control")
def trade_control(user=Depends(require_role("admin", "trader"))):
    return {
        "message": "Trading access granted",
        "role": user["role"]
    }
    
@router.get("/profile")
def profile(user=Depends(get_current_user)):
    return {
        "username": user["sub"],
        "role": user["role"]
    }

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

POST /login
{
  "username": "admin",
  "password": "admin123"
}