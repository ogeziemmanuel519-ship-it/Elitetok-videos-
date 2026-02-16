from fastapi import APIRouter, Request, Header
import os

router = APIRouter()
KOFI_SECRET = os.getenv("KOFI_SECRET", "supersecretkofi")

@router.post("/kofi-webhook")
async def kofi_webhook(request: Request, verification: str = Header(...)):
    if verification != KOFI_SECRET:
        return {"error": "Invalid secret"}
    data = await request.json()
    return {"success": True}