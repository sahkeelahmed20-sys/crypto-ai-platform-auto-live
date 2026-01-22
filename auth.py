from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TEMP in-memory admin (we can move to DB later)
ADMIN_USER = {
    "username": "admin",
    "password_hash": pwd_context.hash("admin123")
}

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    try:
        if data.username != ADMIN_USER["username"]:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not pwd_context.verify(data.password, ADMIN_USER["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # TEMP token (JWT comes next)
        token = "demo-token-admin"

        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        print("LOGIN ERROR:", e)
        raise HTTPException(status_code=500, detail="Login failed")