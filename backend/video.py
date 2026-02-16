from fastapi import APIRouter, Header, HTTPException
import jwt
import os
from backend.auth import users

router = APIRouter()
JWT_SECRET = os.environ.get("JWT_SECRET", "supersecret")

@router.post("/analyze")
def analyze_video(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        email = payload["email"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if users[email]["coins"] < 5:
        raise HTTPException(status_code=400, detail="Not enough coins")
    
    users[email]["coins"] -= 5
    # Here you would add AI video analysis logic
    rating = 4.5  # Example AI rating
    
    return {"coins": users[email]["coins"], "ai_rating": rating}