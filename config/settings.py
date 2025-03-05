import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # Camera Configuration
    camera_url: str = os.getenv("CAMERA_URL", "0")
    max_unrecognized: int = int(os.getenv("MAX_UNRECOGNIZED", 3))
    
    # Firebase
    firebase_key_path: str = os.getenv("FIREBASE_KEY_PATH")
    firebase_db_url: str = os.getenv("FIREBASE_DATABASE_URL")
    
    # Twilio
    twilio_sid: str = os.getenv("TWILIO_SID")
    twilio_token: str = os.getenv("TWILIO_TOKEN")
    twilio_number: str = os.getenv("TWILIO_NUMBER")
    user_number: str = os.getenv("USER_NUMBER")

settings = Settings()