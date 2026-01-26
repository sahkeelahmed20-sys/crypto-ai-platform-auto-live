from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from auth import router as auth_router
from stats import router as stats_router
import time
from market import router as market_router
from trades import router as trades_router



app = FastAPI(title="Crypto AI Platform")

Base.metadata.create_all(bind=engine)

app.include_router(trades_router)

app.include_router(market_router)

app.include_router(stats_router)

app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/market/candles")
def get_candles(symbol: str):
    # TEMP: mock candles (we replace with real exchange next)
    now = int(time.time())
    candles = []

    price = 43000
    for i in range(60):
        open_ = price
        close = open_ + (-200 + i * 5)
        high = max(open_, close) + 50
        low = min(open_, close) - 50

        candles.append({
            "time": now - (60 - i) * 60,
            "open": open_,
            "high": high,
            "low": low,
            "close": close
        })
        price = close

    return candles
    
@app.get("/stats/summary")
def stats_summary():
    return {
        "total_trades": 0,
        "win_rate": 0,
        "pnl": 0
    }

@app.get("/")
def root():
    return {"status": "ok"}