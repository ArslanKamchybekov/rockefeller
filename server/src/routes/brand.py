from fastapi import APIRouter, HTTPException
from src.agents.branding import generate_branding, generate_branding_video
from ..models.branding import BrandingInfoInput, BrandingInfosOutput, BrandingInfoVideoOutput

router = APIRouter(prefix="/api/branding", tags=["branding"])

@router.post("/generate", response_model=BrandingInfosOutput)
async def generate_branding_assets(input: BrandingInfoInput):
    """
    Generate branding assets (logo, tagline, name) for a business idea.
    """
    try:
        result = generate_branding(input.idea_string)
        return BrandingInfosOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating branding documents: {str(e)}")


@router.post("/generate-video", response_model=BrandingInfoVideoOutput)
async def generate_branding_video_asset(input: BrandingInfoInput):
    """
    Generate branding video for a business idea.
    """
    try:
        result = generate_branding_video(input.idea_string)
        return BrandingInfoVideoOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating branding video: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "branding"}