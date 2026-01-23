from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from auth import router as auth_router

app = FastAPI(title="Crypto AI Platform")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"status": "ok", "service": "Crypto AI Platform"}