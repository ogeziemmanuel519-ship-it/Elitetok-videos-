from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt, time, os

router = APIRouter()
SECRET = os.getenv("JWT_SECRET", "supersecret")
users_db = {}  # email -> {password, coins, referrer}

class AuthModel(BaseModel):
    email: str
    password: str
    ref: str = ""

def create_token(email: str):
    payload = {"email": email, "exp": time.time() + 3600*24*7}
    return jwt.encode(payload, SECRET, algorithm="HS256")

@router.post("/signup")
def signup(data: AuthModel):
    if data.email in users_db:
        raise HTTPException(status_code=400, detail="User exists")
    users_db[data.email] = {"password": data.password, "coins": 10, "referrer": data.ref}
    if data.ref and data.ref in users_db:
        users_db[data.ref]["coins"] += 10
        users_db[data.email]["coins"] += 20
    return {"message": "Signup successful"}

@router.post("/login")
def login(data: AuthModel):
    user = users_db.get(data.email)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(data.email)
    return {"token": token, "coins": user["coins"]}