from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ PRE-GENERATED HASH (STATIC, SAFE)
# This hash is for password: admin123
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = "$2b$12$yFv0Xy4tCw8vZKx7xK9f6O6FzF0Qy6y6mZxZp0QFz9cFQXzq8Kk6e"


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest):
    if data.username != ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ ONLY VERIFY — NO HASHING
    if not pwd_context.verify(data.password, ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": "demo-token-admin",
        "token_type": "bearer"
    }