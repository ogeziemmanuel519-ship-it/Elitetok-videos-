from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from auth import create_access_token, decode_access_token
from database import users, referral_codes, User
from schemas import SignupRequest, LoginRequest, AnalyzeRequest
from utils import generate_referral_code, ai_rate_video
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================
# Signup
# =======================
@app.post("/api/signup")
def signup(req: SignupRequest):
    if req.email in users:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = pwd_context.hash(req.password)
    referral_code = generate_referral_code(req.email)

    coins = 1000  # New user starting coins for £10 purchase
    referred_by = None

    # Handle referral bonus
    if req.referral and req.referral in referral_codes:
        ref_email = referral_codes[req.referral]
        users[ref_email].coins += 10  # Referrer bonus
        coins += 10  # New user referral bonus
        referred_by = ref_email

    user = User(
        username=req.username,
        email=req.email,
        password=hashed_password,
        coins=coins,
        referral_code=referral_code,
        referred_by=referred_by
    )

    users[req.email] = user
    referral_codes[referral_code] = req.email

    token = create_access_token({"sub": req.email})
    return {"token": token, "coins": user.coins, "referral_code": referral_code}

# =======================
# Login
# =======================
@app.post("/api/login")
def login(req: LoginRequest):
    user = users.get(req.email)
    if not user or not pwd_context.verify(req.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": req.email})
    return {"token": token, "coins": user.coins}

# =======================
# Video Analysis
# =======================
@app.post("/api/analyze")
async def analyze(token: str = Form(...), link: str = Form(None), file: UploadFile = File(None)):
    email = decode_access_token(token)
    if not email or email not in users:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = users[email]
    if user.coins < 5:
        raise HTTPException(status_code=400, detail="Not enough coins")

    # Deduct coins
    user.coins -= 5

    # Fake AI rating
    rating = ai_rate_video()

    return {"ai_rating": rating, "coins": user.coins}