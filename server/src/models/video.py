from pydantic import BaseModel
from typing import Any

class VideoInput (BaseModel):
    prompt: str

class VideoOutput (BaseModel):
    video: Any