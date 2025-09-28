from fastapi import APIRouter, HTTPException
from src.agents.researchers import MarketResearchCrew
from ..models.research_output import MarketResearchOutput, BusinessIdeaInput
from ..agents.docs import generate_legal_docs

router = APIRouter(prefix="/api/research", tags=["research"])

@router.post("/generate", response_model=MarketResearchOutput)
async def generate_research(input: BusinessIdeaInput):
    """
    Generate legal documents (Privacy Policy, Terms of Use, NDA) for a business idea.
    """
    try:
        crew = MarketResearchCrew()
        result = crew.research(input.idea)
        return MarketResearchOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating research: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "research"}
