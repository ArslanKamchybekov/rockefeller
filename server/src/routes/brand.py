from fastapi import APIRouter, HTTPException
from src.agents.branding import generate_branding
from ..models.branding import BrandingInfoInput, BrandingInfosOutput, BrandingInfoVideoOutput

router = APIRouter(prefix="/api/branding", tags=["branding"])

@router.post("/generate", response_model=BrandingInfosOutput)
async def generate_branding_documents(input: BrandingInfoInput):
    """
    Generate branding documents (logo, tagline, name) for a business idea.
    """
    try:
        result = generate_branding(input.idea_string)
        return BrandingInfosOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating branding documents: {str(e)}")


@router.post("/generate-video", response_model=BrandingInfoVideoOutput)
async def generate_branding_video(input: BrandingInfoInput):
    """
    Generate branding video for a business idea.
    """
    try:
        result = generate_branding(input.idea_string)
        # For now, return the same branding data with a placeholder video URL
        # In the future, this could generate an actual video
        video_result = {
            "branding": result["branding"],
            "video_url": None  # Placeholder for future video generation
        }
        return BrandingInfoVideoOutput(**video_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating branding video: {str(e)}")
    
@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "branding"}