import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.auth import router as auth_router
from backend.ai import router as ai_router
from backend.kofi import router as kofi_router

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(auth_router, prefix="/api")
app.include_router(ai_router, prefix="/api")
app.include_router(kofi_router, prefix="/api")

# Serve frontend build
app.mount("/", StaticFiles(directory="frontend/build", html=True), name="frontend")