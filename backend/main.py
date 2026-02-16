import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.auth import router as auth_router
from backend.video import router as video_router
from backend.payment import router as payment_router

app = FastAPI(title="EliteTok Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# API Routers
app.include_router(auth_router, prefix="/api")
app.include_router(video_router, prefix="/api")
app.include_router(payment_router, prefix="/api")

# Serve frontend
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(current_dir, "..", "frontend")
frontend_path = os.path.abspath(frontend_path)

if not os.path.exists(frontend_path):
    raise RuntimeError(f"Frontend directory '{frontend_path}' does not exist!")

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/ping")
def ping():
    return {"message": "Backend running!"}