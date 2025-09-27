import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL)

def create_gemini_client():
    return model