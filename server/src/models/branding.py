from pydantic import BaseModel

class BrandingInfoInput (BaseModel):
    idea_string : str

class BrandingInfosOutput (BaseModel):
    branding : dict 

class BrandingInfoVideoOutput (BaseModel):
    video : bytes