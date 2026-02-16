import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import API routers
from backend.auth import router as auth_router
from backend.ai import router as ai_router
from backend.kofi import router as kofi_router

app = FastAPI(title="EliteTok Backend")

# --- CORS for frontend fetch calls ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- API Routes ---
app.include_router(auth_router, prefix="/api")
app.include_router(ai_router, prefix="/api")
app.include_router(kofi_router, prefix="/api")

# --- Serve static frontend correctly ---
# Absolute path calculation, works on Render
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(current_dir, "..", "frontend")
frontend_path = os.path.abspath(frontend_path)

if not os.path.exists(frontend_path):
    raise RuntimeError(f"Frontend directory '{frontend_path}' does not exist!")

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

# --- Optional root route ---
@app.get("/ping")
def ping():
    return {"message": "Backend is running!"}