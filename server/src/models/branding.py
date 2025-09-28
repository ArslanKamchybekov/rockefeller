from pydantic import BaseModel

class BrandingInfoInput (BaseModel):
    marketData: str

class BrandingInfosOutput (BaseModel):
   businessData : {image : image,
                    name : name,
                    slogan : slogan}