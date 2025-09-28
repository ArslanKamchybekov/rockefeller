from pydantic import BaseModel
from typing import Any

class BrandingInfoInput (BaseModel):
    idea_string : str

class BrandingInfosOutput (BaseModel):
    branding : dict 

class BrandingInfoVideoOutput (BaseModel):
    video: Any
    video_url: str | None = None