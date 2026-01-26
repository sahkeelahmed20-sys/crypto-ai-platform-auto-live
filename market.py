from fastapi import APIRouter
import time

router = APIRouter(prefix="/market")

@router.get("/candles")
def candles():
    return [
        {"time": int(time.time()), "open": 43000, "high": 43500, "low": 42800, "close": 43200}
    ]