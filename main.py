from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from market import router as market_router

app = FastAPI(title="Crypto AI Platform")

app.include_router(market_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")