import httpx, time
from fastapi import APIRouter, Query

router = APIRouter(prefix="/market", tags=["Market"])

BINANCE = "https://api.binance.com"

def ema(values, period):
    k = 2 / (period + 1)
    ema_vals = []
    for i, v in enumerate(values):
        ema_vals.append(v if i == 0 else v * k + ema_vals[-1] * (1 - k))
    return ema_vals

def rsi(values, period=14):
    gains, losses = [], []
    rsis = [None] * len(values)
    for i in range(1, len(values)):
        d = values[i] - values[i-1]
        gains.append(max(d, 0))
        losses.append(abs(min(d, 0)))
        if i >= period:
            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period or 1e-9
            rs = avg_gain / avg_loss
            rsis[i] = 100 - (100 / (1 + rs))
    return rsis

@router.get("/candles")
async def candles(
    symbol: str = Query("BTCUSDT"),
    interval: str = Query("1m"),
    limit: int = Query(200)
):
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{BINANCE}/api/v3/klines",
                        params={"symbol": symbol, "interval": interval, "limit": limit})
        k = r.json()

    closes = [float(x[4]) for x in k]
    ema20 = ema(closes, 20)
    rsi14 = rsi(closes, 14)

    data = []
    for i, x in enumerate(k):
        data.append({
            "time": int(x[0] / 1000),
            "open": float(x[1]),
            "high": float(x[2]),
            "low": float(x[3]),
            "close": float(x[4]),
            "ema20": ema20[i],
            "rsi14": rsi14[i]
        })
    return data
