import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-vision-1.0")

if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL)
image_model = genai.GenerativeModel(IMAGE_MODEL)

def create_gemini_client():
    return model

def create_gemini_image_client():
    return image_model