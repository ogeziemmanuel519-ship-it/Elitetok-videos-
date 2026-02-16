from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt
import os

router = APIRouter()

JWT_SECRET = os.environ.get("JWT_SECRET", "supersecret")

# In-memory "database" for demo purposes
users = {}

class SignupModel(BaseModel):
    username: str
    email: str
    password: str
    referral: str = None

class LoginModel(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(data: SignupModel):
    if data.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # New user coins: 1000 coins
    coins = 1000
    users[data.email] = {
        "username": data.username,
        "password": data.password,
        "coins": coins
    }
    
    # Referral bonus: 10 coins to new user + 10 to referrer
    if data.referral and data.referral in users:
        users[data.referral]["coins"] += 10
        users[data.email]["coins"] += 10
    
    token = jwt.encode({"email": data.email}, JWT_SECRET, algorithm="HS256")
    return {"token": token, "coins": users[data.email]["coins"]}

@router.post("/login")
def login(data: LoginModel):
    if data.email not in users or users[data.email]["password"] != data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = jwt.encode({"email": data.email}, JWT_SECRET, algorithm="HS256")
    return {"token": token, "coins": users[data.email]["coins"]}