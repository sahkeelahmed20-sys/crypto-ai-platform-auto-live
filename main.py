from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_engine import get_all_signals
from auto_trader import auto_trade

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DEMO_USER = {
    "api_key": "honFOrqroKOVb0DFSCzHqZYvwGeymNQy3EFgF35SmVg1ceiSWZ7E9E3odeJuaAOc",
    "api_secret": "p1y7rzg89su3jYWnmIgHjnP1Ov1XcH70kwExswK5PYRFvUFVwQNZIm6dZ4QNVGjj",
    "balance": 1000,
    "auto_trade": True
}

@app.get("/")
def root():
    return {"status": "ok", "message": "Crypto AI is live"}

@app.get("/signals")
def signals():
    results = []
    for s in get_all_signals():
        try:
            trade = auto_trade(s, DEMO_USER)
        except Exception as e:
            trade = {"error": str(e)}
        s["auto"] = trade
        results.append(s)
    return results
    from binance_data import get_price_history

@app.get("/debug")
def debug():
    df = get_price_history("BTCUSDT", "5m")
    return {
        "last_close": df["close"].iloc[-1],
        "rows": len(df)
    }
