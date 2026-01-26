import httpx, time
from fastapi import APIRouter, Query

router = APIRouter(prefix="/market", tags=["Market"])

BINANCE_URL = "https://api.binance.com/api/v3/klines"

@router.get("/candles")
async def get_candles(symbol: str = "BTCUSDT", interval: str = "1h"):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 100
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(BINANCE_URL, params=params)
        data = r.json()

    return 
        {
            "time": c[0],
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5])
        }
        for c in data
        
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
    
def vwap(candles):
    cumulative_pv = 0
    cumulative_vol = 0
    vwaps = []

    for c in candles:
        typical_price = (c["high"] + c["low"] + c["close"]) / 3
        volume = c.get("volume", 1)  # Binance gives volume
        cumulative_pv += typical_price * volume
        cumulative_vol += volume
        vwaps.append(cumulative_pv / cumulative_vol)

    return vwaps


def macd(values, fast=12, slow=26, signal=9):
    def ema(vals, period):
        k = 2 / (period + 1)
        e = []
        for i, v in enumerate(vals):
            e.append(v if i == 0 else v * k + e[-1] * (1 - k))
        return e

    ema_fast = ema(values, fast)
    ema_slow = ema(values, slow)

    macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
    signal_line = ema(macd_line, signal)
    hist = [m - s for m, s in zip(macd_line, signal_line)]

    return macd_line, signal_line, hist

@router.get("/candles")
async def candles(symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 200):
    async with httpx.AsyncClient() as c:
        r = await c.get(
            f"{BINANCE}/api/v3/klines",
            params={"symbol": symbol, "interval": interval, "limit": limit}
        )
        k = r.json()

    candles = []
    closes = []

    for x in k:
        candles.append({
            "time": int(x[0] / 1000),
            "open": float(x[1]),
            "high": float(x[2]),
            "low": float(x[3]),
            "close": float(x[4]),
            "volume": float(x[5])
        })
        closes.append(float(x[4]))

    ema20 = ema(closes, 20)
    rsi14 = rsi(closes, 14)
    vwap_vals = vwap(candles)
    macd_line, signal_line, hist = macd(closes)

    for i in range(len(candles)):
        candles[i].update({
            "ema20": ema20[i],
            "rsi14": rsi14[i],
            "vwap": vwap_vals[i],
            "macd": macd_line[i],
            "macd_signal": signal_line[i],
            "macd_hist": hist[i]
        })

    return candles