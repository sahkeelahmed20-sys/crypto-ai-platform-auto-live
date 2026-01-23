from fastapi import FastAPI
from auth import router as auth_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Crypto AI Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTERS MUST COME AFTER app EXISTS
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Crypto AI Platform",
        "message": "Backend is running"
    }