from pydantic import BaseModel

class VideoInput (BaseModel):
    prompt: str

class VideoOutput (BaseModel):
    : str