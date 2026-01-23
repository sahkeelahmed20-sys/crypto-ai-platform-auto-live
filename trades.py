from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/trades", tags=["Trades"])

# TEMP in-memory (swap to DB later)
TRADES = [
    {"id": 1, "side": "BUY",  "price": 43000, "time": 1700000000},
    {"id": 2, "side": "SELL", "price": 43500, "time": 1700003600},
]

@router.get("/")
def list_trades():
    return TRADES

@router.get("/pnl")
def pnl():
    pnl = 0
    last_buy = None
    for t in TRADES:
        if t["side"] == "BUY":
            last_buy = t["price"]
        elif t["side"] == "SELL" and last_buy:
            pnl += t["price"] - last_buy
            last_buy = None
    return {"pnl": pnl}