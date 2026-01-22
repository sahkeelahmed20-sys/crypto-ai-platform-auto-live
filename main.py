from users import register_user, authenticate
from models import init_db
from jose import jwt
from config import JWT_SECRET, JWT_ALGORITHM
from fastapi import Header, HTTPException
from auth import authenticate, create_token, verify_token
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_engine import get_all_signals
from auto_trader import auto_trade
from fastapi import Depends, Header, HTTPException
from config import AUTO_TRADING_STATE
from stats import get_stats
from auth import authenticate, create_token, verify_token

def require_auth(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user

app=FastAPI()
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

trade = auto_trade(s, DEMO_USER)
log_trade(s, trade)

@app.get("/signals")
def signals():
    try:
        signals = get_all_signals()
        return {
            "count": len(signals),
            "signals": signals
        }
    except Exception as e:
        return {
            "error": str(e),
            "type": type(e).__name__
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
@app.post("/login")
def login(data: dict):
    token = authenticate(data["username"], data["password"])
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": token}
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