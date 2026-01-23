from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from auth import router as auth_router
from stats import router as stats_router

app = FastAPI(title="Crypto AI Platform")

Base.metadata.create_all(bind=engine)

app.include_router(stats_router)

app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"status": "ok"}