from fastapi import FastAPI
from auth import router as auth_router

app = FastAPI(title="Crypto AI Platform")

# ✅ ROUTERS MUST COME AFTER app EXISTS
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Crypto AI Platform",
        "message": "Backend is running"
    }