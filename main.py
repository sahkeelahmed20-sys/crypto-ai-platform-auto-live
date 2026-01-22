
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_engine import get_all_signals
from auto_trader import auto_trade

app=FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

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

@app.get("/debug")
def debug():
    df = get_price_history("BTCUSDT", "5m")
    return {
        "last_close": df["close"].iloc[-1],
        "rows": len(df)
    }
    
    
    from config import AUTO_TRADING_STATE

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