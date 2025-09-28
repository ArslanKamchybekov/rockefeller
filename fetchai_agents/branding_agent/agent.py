"""
Branding Agent for Fetch.ai AgentVerse
Creates logos, taglines, color schemes, and visual assets
"""

from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from pydantic import BaseModel
import requests
import json
import os
from typing import List, Dict, Any, Optional
import asyncio

# Agent configuration
BRANDING_AGENT = Agent(
    name="branding_agent",
    seed="branding-agent-seed-phrase-12345",
    port=8002,
    endpoint=["http://localhost:8002/submit"],
)

# Pydantic models
class BrandingRequest(BaseModel):
    business_idea: str
    industry: str
    target_audience: str
    brand_personality: List[str] = ["professional", "modern"]
    color_preferences: Optional[List[str]] = None
    style_preferences: Optional[List[str]] = None

class BrandingResponse(BaseModel):
    success: bool
    brand_name: str
    tagline: str
    color_scheme: Dict[str, str]
    logo_description: str
    brand_guidelines: Dict[str, Any]
    visual_assets: List[Dict[str, Any]]
    brand_personality: Dict[str, Any]

class ErrorResponse(BaseModel):
    success: bool
    error: str

@BRANDING_AGENT.on_message(model=BrandingRequest)
async def handle_branding_request(ctx: Context, sender: str, msg: BrandingRequest):
    """Handle branding generation requests"""
    try:
        ctx.logger.info(f"Received branding request for {msg.business_idea}")
        
        # Generate branding assets
        branding_data = await generate_branding_assets(
            business_idea=msg.business_idea,
            industry=msg.industry,
            target_audience=msg.target_audience,
            brand_personality=msg.brand_personality,
            color_preferences=msg.color_preferences,
            style_preferences=msg.style_preferences
        )
        
        response = BrandingResponse(
            success=True,
            brand_name=branding_data["brand_name"],
            tagline=branding_data["tagline"],
            color_scheme=branding_data["color_scheme"],
            logo_description=branding_data["logo_description"],
            brand_guidelines=branding_data["brand_guidelines"],
            visual_assets=branding_data["visual_assets"],
            brand_personality=branding_data["brand_personality"]
        )
        
        await ctx.send(sender, response.model_dump())
        ctx.logger.info(f"Sent branding response to {sender}")
        
    except Exception as e:
        ctx.logger.error(f"Error in branding generation: {e}")
        error_response = ErrorResponse(success=False, error=str(e))
        await ctx.send(sender, error_response.model_dump())

async def generate_branding_assets(
    business_idea: str,
    industry: str,
    target_audience: str,
    brand_personality: List[str],
    color_preferences: Optional[List[str]] = None,
    style_preferences: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Generate comprehensive branding assets"""
    
    # Generate brand name based on business idea
    brand_name = generate_brand_name(business_idea, industry)
    
    # Generate tagline
    tagline = generate_tagline(business_idea, brand_personality)
    
    # Generate color scheme
    color_scheme = generate_color_scheme(industry, brand_personality, color_preferences)
    
    # Generate logo description
    logo_description = generate_logo_description(brand_name, industry, brand_personality)
    
    # Create brand guidelines
    brand_guidelines = {
        "logo_usage": {
            "minimum_size": "100px",
            "clear_space": "50px",
            "backgrounds": ["white", "black", "primary_color"],
            "prohibited": ["stretching", "distorting", "recoloring"]
        },
        "typography": {
            "primary_font": "Inter" if "modern" in brand_personality else "Roboto",
            "secondary_font": "Open Sans",
            "headings": "Bold, 24px+",
            "body": "Regular, 16px"
        },
        "voice_tone": {
            "personality": brand_personality,
            "tone": "professional" if "professional" in brand_personality else "friendly",
            "style": "conversational" if "friendly" in brand_personality else "formal"
        }
    }
    
    # Generate visual assets
    visual_assets = [
        {
            "type": "logo",
            "description": logo_description,
            "formats": ["PNG", "SVG", "PDF"],
            "variations": ["horizontal", "vertical", "icon"]
        },
        {
            "type": "business_cards",
            "description": f"Professional business cards for {brand_name}",
            "elements": ["logo", "contact_info", "tagline"]
        },
        {
            "type": "social_media_templates",
            "description": f"Social media templates for {brand_name}",
            "platforms": ["Instagram", "LinkedIn", "Twitter"]
        }
    ]
    
    # Brand personality analysis
    brand_personality_analysis = {
        "traits": brand_personality,
        "values": extract_brand_values(business_idea, industry),
        "target_emotions": ["trust", "excitement", "reliability"],
        "messaging_framework": {
            "headline": f"{brand_name}: {tagline}",
            "subheading": f"Transforming {industry} with innovative solutions",
            "call_to_action": "Get started today"
        }
    }
    
    return {
        "brand_name": brand_name,
        "tagline": tagline,
        "color_scheme": color_scheme,
        "logo_description": logo_description,
        "brand_guidelines": brand_guidelines,
        "visual_assets": visual_assets,
        "brand_personality": brand_personality_analysis
    }

def generate_brand_name(business_idea: str, industry: str) -> str:
    """Generate a brand name based on business idea and industry"""
    # Simple brand name generation (replace with AI-powered generation)
    words = business_idea.lower().split()
    industry_words = industry.lower().split()
    
    # Combine relevant words
    if len(words) >= 2:
        return f"{words[0].capitalize()}{words[1].capitalize()}"
    else:
        return f"{words[0].capitalize()}Tech"

def generate_tagline(business_idea: str, brand_personality: List[str]) -> str:
    """Generate a compelling tagline"""
    taglines = [
        f"Transforming {business_idea} for the modern world",
        f"Your partner in {business_idea} innovation",
        f"Where {business_idea} meets excellence",
        f"Empowering {business_idea} solutions"
    ]
    return taglines[0]  # Return first tagline (replace with AI generation)

def generate_color_scheme(industry: str, brand_personality: List[str], color_preferences: Optional[List[str]] = None) -> Dict[str, str]:
    """Generate a color scheme"""
    if color_preferences:
        return {
            "primary": color_preferences[0] if color_preferences else "#2563eb",
            "secondary": color_preferences[1] if len(color_preferences) > 1 else "#64748b",
            "accent": color_preferences[2] if len(color_preferences) > 2 else "#f59e0b",
            "neutral": "#f8fafc"
        }
    
    # Default color schemes based on industry
    color_schemes = {
        "tech": {"primary": "#2563eb", "secondary": "#64748b", "accent": "#f59e0b", "neutral": "#f8fafc"},
        "healthcare": {"primary": "#059669", "secondary": "#6b7280", "accent": "#dc2626", "neutral": "#f9fafb"},
        "finance": {"primary": "#1f2937", "secondary": "#4b5563", "accent": "#10b981", "neutral": "#f3f4f6"},
        "retail": {"primary": "#7c3aed", "secondary": "#8b5cf6", "accent": "#f59e0b", "neutral": "#fafafa"}
    }
    
    return color_schemes.get(industry.lower(), color_schemes["tech"])

def generate_logo_description(brand_name: str, industry: str, brand_personality: List[str]) -> str:
    """Generate a logo description"""
    style = "modern" if "modern" in brand_personality else "classic"
    return f"A {style} logo for {brand_name} featuring clean typography and {industry}-inspired iconography"

def extract_brand_values(business_idea: str, industry: str) -> List[str]:
    """Extract brand values from business idea"""
    return ["innovation", "quality", "customer_focus", "sustainability"]

@BRANDING_AGENT.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    ctx.logger.info("Branding Agent started")
    ctx.logger.info(f"Agent address: {BRANDING_AGENT.address}")

if __name__ == "__main__":
    fund_agent_if_low(BRANDING_AGENT.wallet.address())
    BRANDING_AGENT.run()
