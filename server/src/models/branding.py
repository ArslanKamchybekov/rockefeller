from pydantic import BaseModel
from typing import Optional

class BrandingInfoInput (BaseModel):
    idea_string : str

class BrandingInfosOutput (BaseModel):
    branding : dict 

class BrandingInfoVideoOutput (BaseModel):
    branding : dict
    video_url : Optional[str] = None