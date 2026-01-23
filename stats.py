from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from trades import Trade

router = APIRouter(prefix="/stats")

@router.get("/history")
def trade_history(db: Session = Depends(get_db)):
    trades = db.query(Trade).all()
    return [
        {
            "pair": t.pair,
            "profit": t.profit,
            "time": t.time
        }
        for t in trades
    ]

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    trades = db.query(Trade).all()
    return {
        "total_trades": len(trades),
        "profit": sum(t.profit for t in trades)
    }