import random

def generate_referral_code(email: str):
    return email.split("@")[0] + str(random.randint(1000,9999))

def ai_rate_video():
    # Placeholder: returns a random rating 0-100
    return round(random.uniform(50, 100), 2)