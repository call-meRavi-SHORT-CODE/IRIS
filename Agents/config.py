import os
from dotenv import load_dotenv

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Set GEMINI_API_KEY in your environment or .env file")