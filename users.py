from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from database import get_db
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(username, password):
    db = get_db()
    hashed = pwd.hash(password)
    db.execute(
        "INSERT INTO users (username, password) VALUES (?,?)",
        (username, hashed)
    )
    db.commit()

def authenticate(username, password):
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if not user or not pwd.verify(password, user["password"]):
        return None

    payload = {
        "id": user["id"],
        "admin": bool(user["is_admin"]),
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token
