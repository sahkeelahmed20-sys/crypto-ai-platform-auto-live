from fastapi import APIRouter, WebSocket
import httpx
import asyncio

router = APIRouter()

BINANCE_URL = "https://api.binance.com/api/v3/klines"

@router.websocket("/ws/market")
async def market_ws(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            params = {
                "symbol": "BTCUSDT",
                "interval": "1m",
                "limit": 1
            }

            async with httpx.AsyncClient() as client:
                r = await client.get(BINANCE_URL, params=params)
                c = r.json()[0]

            candle = {
                "time": c[0] // 1000,
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4])
            }

            await websocket.send_json(candle)
            await asyncio.sleep(5)

        except:
            break
