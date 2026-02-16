from pydantic import BaseModel
from typing import Optional

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str
    referral: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class AnalyzeRequest(BaseModel):
    link: Optional[str] = None