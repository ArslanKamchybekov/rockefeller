from fastapi import APIRouter, HTTPException
from src.agents.branding import generate_branding
from ..models.branding import BrandingInfoInput, BrandingInfosOutput, BrandingInfoVideoOutput

router = APIRouter(prefix="/api/branding", tags=["branding"])

@router.post("/generate", response_model=BrandingInfoInput)
async def generate_branding_documents(input: BrandingInfosOutput):
    """
    Generate branding documents (logo, tagline, name) for a business idea.
    """
    try:
        result = generate_branding(input)
        return BrandingInfosOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating branding documents: {str(e)}")


@router.post("/generate-video", response_model=BrandingInfoInput)
async def generate_branding_documents(input: BrandingInfoVideoOutput):
    """
    Generate branding documents (video) for a business idea.
    """
    try:
        result = generate_branding(input)
        return BrandingInfoVideoOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating branding video documents: {str(e)}")
    
@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "branding"}