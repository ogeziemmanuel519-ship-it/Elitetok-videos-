from typing import Dict
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str
    coins: int = 0
    referral_code: str = None
    referred_by: str = None

users: Dict[str, User] = {}  # key=email
referral_codes: Dict[str, str] = {}  # key=referral_code, value=email