from fastapi import APIRouter, UploadFile, File, Header
import random

router = APIRouter()

@router.post("/analyze")
def analyze_video(file: UploadFile = File(...), token: str = Header(...)):
    # Deduct coins logic can go here
    return {"score": random.randint(50,100), "engagement": random.randint(50,100)}

@router.post("/thumbnail-score")
def thumbnail_score(file: UploadFile = File(...), token: str = Header(...)):
    return {"score": random.randint(50,100), "brightness": random.randint(0,100)}