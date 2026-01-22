from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from config import ADMIN_USER, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash admin password once
def authenticate(username: str, password: str):
    if username != ADMIN_USER["username"]:
        return False

    # compare raw password (safe for admin-only setup)
    return password == ADMIN_USER["password"]

def authenticate(username: str, password: str):
    if username != ADMIN_USER["username"]:
        return False
    return pwd_context.verify(password, ADMIN_HASH)

def create_token():
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": ADMIN_USER["username"], "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except JWTError:
        return None
