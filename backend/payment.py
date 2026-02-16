from fastapi import APIRouter, Request
from backend.auth import users

router = APIRouter()

# Ko-fi / PayPal webhook
@router.post("/kofi-webhook")
async def kofi_webhook(req: Request):
    data = await req.json()
    email = data.get("email")
    coins = int(data.get("coins", 0))
    
    if email in users:
        users[email]["coins"] += coins
        return {"status": "success", "coins": users[email]["coins"]}
    return {"status": "user not found"}