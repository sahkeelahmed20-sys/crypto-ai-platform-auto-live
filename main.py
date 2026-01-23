from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from users import register_user, authenticate
from models import init_db
from jose import jwt
from config import JWT_SECRET, JWT_ALGORITHM
from fastapi import Header, HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_engine import get_all_signals
from auto_trader import auto_trade
from fastapi import Depends, Header, HTTPException
from config import AUTO_TRADING_STATE
from stats import get_stats
from auth import router as auth_router
app.include_router(auth_router)


from fastapi import FastAPI
from auth import router as auth_router

app = FastAPI(title="Crypto AI Platform")

# ✅ INCLUDE ROUTERS AFTER app IS CREATED
app.include_router(auth_router)

# ---- OPTIONAL ROOT ENDPOINT ----
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Crypto AI Platform",
        "message": "Backend is running"
    }

def require_auth(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user


app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return Path("frontend/index.html").read_text()  
from jose import jwt
from config import JWT_SECRET, JWT_ALGORITHM
from fastapi import Header, HTTPException

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
init_db()   
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
     
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Crypto AI Platform",
        "message": "Backend is running"
    }
@app.post("/register")
def register(data: dict):
    register_user(data["username"], data["password"])
    return {"status": "user_created"}
    
@app.get("/users")
def list_users(user=Depends(get_current_user)):
    if not user["admin"]:
        raise HTTPException(status_code=403)

    db = get_db()
    users = db.execute(
        "SELECT id, username, is_admin, auto_trading FROM users"
    ).fetchall()

    return [dict(u) for u in users]
    
DEMO_USER={
 "api_key":"JkUZNQbfPbdpWGYdC0Cxv0bXczcyLy5ExJHFU0zy78ZdhUHAPRlfzmd2GIfdBU0j",
 "api_secret":"ojJMIVGoAhItzWGMKJ4HrbrG1egikeCZf8Ith5AShSz3sqBMsLuzDwVP9EhbBHU9",
 "balance":1000,
 "auto_trade":True
}

from stats import log_trade

@app.get("/signals")
def signals():
    results = []

    all_signals = get_all_signals()

    for sig in all_signals:
        try:
            trade = auto_trade(sig, DEMO_USER)
        except Exception as e:
            trade = {"error": str(e)}

        sig["auto"] = trade
        results.append(sig) 

    return {
        "count": len(results),
        "signals": results
    }
    
    from binance_data import get_price_history
    
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401)

    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return payload 
    
@app.post("/control/enable")
def enable_trading(user=Depends(get_current_user)):
    if not user["admin"]:
        raise HTTPException(status_code=403)
    AUTO_TRADING_STATE["enabled"] = True
    return {"auto_trading": True}
    
@app.get("/control/status")
def control_status(user=Depends(require_auth)):
    return {"auto_trading": AUTO_TRADING_STATE["enabled"]}

@app.post("/control/enable")
def enable_trading(user=Depends(require_auth)):
    AUTO_TRADING_STATE["enabled"] = True
    return {"auto_trading": True}

@app.post("/control/disable")
def disable_trading(user=Depends(require_auth)):
    AUTO_TRADING_STATE["enabled"] = False
    return {"auto_trading": False}

@app.get("/stats")
def stats(user=Depends(require_auth)):
    return get_stats()

@app.get("/debug")
def debug():
    df = get_price_history("BTCUSDT", "5m")
    return {
        "last_close": df["close"].iloc[-1],
        "rows": len(df)
    }
    
    
    from config import AUTO_TRADING_STATE

from fastapi import HTTPException

@app.post("/login")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(
            status_code=422,
            detail="username and password are required"
        )

    if username != ADMIN_USER["username"] or password != ADMIN_USER["password"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = jwt.encode(
        {"sub": username},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/control/status")
def control_status():
    return {
        "auto_trading": AUTO_TRADING_STATE["enabled"]
    }

@app.post("/control/enable")
def enable_trading():
    AUTO_TRADING_STATE["enabled"] = True
    return {"auto_trading": True}

@app.post("/control/disable")
def disable_trading():
    AUTO_TRADING_STATE["enabled"] = False
    return {"auto_trading": False}
    
from stats import get_stats

@app.get("/stats")
def stats():
    return get_stats()
def require_auth(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user