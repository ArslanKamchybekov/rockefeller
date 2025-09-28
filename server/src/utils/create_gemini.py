from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash")
VIDEO_MODEL = os.getenv("GEMINI_VIDEO_MODEL", "veo-3.0-generate-001")

if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY")


client = genai.Client(api_key=API_KEY)

def create_gemini_client():
    return MODEL, client

def create_gemini_image_client():
    return IMAGE_MODEL, client

def create_gemini_video_client():
    return VIDEO_MODEL, client