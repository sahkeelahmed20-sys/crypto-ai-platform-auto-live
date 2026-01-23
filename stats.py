from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter(prefix="/stats", tags=["Stats"])

# TEMP: replace later with database
TRADES = [
    {"time": datetime.now() - timedelta(minutes=30), "profit": 12},
    {"time": datetime.now() - timedelta(minutes=20), "profit": -5},
    {"time": datetime.now() - timedelta(minutes=10), "profit": 20},
]

@router.get("/summary")
def stats_summary():
    total = len(TRADES)
    wins = len([t for t in TRADES if t["profit"] > 0])
    profit = sum(t["profit"] for t in TRADES)

    return {
        "total_trades": total,
        "win_rate": round((wins / total) * 100, 2),
        "profit": profit
    }

@router.get("/chart")
def stats_chart():
    return {
        "labels": [t["time"].strftime("%H:%M") for t in TRADES],
        "profits": [t["profit"] for t in TRADES]
    }