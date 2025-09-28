"""
Pitch Deck Agent for Fetch.ai AgentVerse
Builds PDF investor-ready deck and financial model
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
PITCH_DECK_AGENT = Agent(
    name="pitch_deck_agent",
    seed="pitch-deck-agent-seed-phrase-12345",
    port=8008,
    endpoint=["http://localhost:8008/submit"],
)

# Pydantic models
class PitchDeckRequest(BaseModel):
    business_name: str
    industry: str
    business_idea: str
    problem_statement: str
    solution: str
    target_market: str
    business_model: str
    funding_amount: float
    team_info: List[Dict[str, str]]
    financial_projections: Optional[Dict[str, Any]] = None
    competitive_advantage: Optional[str] = None
    traction: Optional[Dict[str, Any]] = None

class PitchDeckResponse(BaseModel):
    success: bool
    pitch_deck_url: str
    slides: List[Dict[str, Any]]
    financial_model: Dict[str, Any]
    investor_notes: List[str]
    presentation_script: List[Dict[str, Any]]
    next_steps: List[str]

class ErrorResponse(BaseModel):
    success: bool
    error: str

@PITCH_DECK_AGENT.on_message(model=PitchDeckRequest)
async def handle_pitch_deck_request(ctx: Context, sender: str, msg: PitchDeckRequest):
    """Handle pitch deck generation requests"""
    try:
        ctx.logger.info(f"Received pitch deck request for {msg.business_name}")
        
        # Generate pitch deck and financial model
        pitch_data = await generate_pitch_deck_and_financials(
            business_name=msg.business_name,
            industry=msg.industry,
            business_idea=msg.business_idea,
            problem_statement=msg.problem_statement,
            solution=msg.solution,
            target_market=msg.target_market,
            business_model=msg.business_model,
            funding_amount=msg.funding_amount,
            team_info=msg.team_info,
            financial_projections=msg.financial_projections,
            competitive_advantage=msg.competitive_advantage,
            traction=msg.traction
        )
        
        response = PitchDeckResponse(
            success=True,
            pitch_deck_url=pitch_data["pitch_deck_url"],
            slides=pitch_data["slides"],
            financial_model=pitch_data["financial_model"],
            investor_notes=pitch_data["investor_notes"],
            presentation_script=pitch_data["presentation_script"],
            next_steps=pitch_data["next_steps"]
        )
        
        await ctx.send(sender, response.model_dump())
        ctx.logger.info(f"Sent pitch deck response to {sender}")
        
    except Exception as e:
        ctx.logger.error(f"Error in pitch deck generation: {e}")
        error_response = ErrorResponse(success=False, error=str(e))
        await ctx.send(sender, error_response.model_dump())

async def generate_pitch_deck_and_financials(
    business_name: str,
    industry: str,
    business_idea: str,
    problem_statement: str,
    solution: str,
    target_market: str,
    business_model: str,
    funding_amount: float,
    team_info: List[Dict[str, str]],
    financial_projections: Optional[Dict[str, Any]] = None,
    competitive_advantage: Optional[str] = None,
    traction: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Generate comprehensive pitch deck and financial model"""
    
    # Generate pitch deck slides
    slides = create_pitch_deck_slides(
        business_name, industry, business_idea, problem_statement,
        solution, target_market, business_model, funding_amount,
        team_info, competitive_advantage, traction
    )
    
    # Create financial model
    financial_model = create_financial_model(
        business_model, funding_amount, financial_projections, industry
    )
    
    # Generate investor notes
    investor_notes = create_investor_notes(
        business_name, industry, funding_amount, team_info, traction
    )
    
    # Create presentation script
    presentation_script = create_presentation_script(slides, business_name)
    
    # Generate next steps
    next_steps = create_next_steps(funding_amount, industry)
    
    # Simulate PDF generation (replace with actual PDF generation)
    pitch_deck_url = f"https://example.com/pitch-decks/{business_name.lower().replace(' ', '-')}-pitch-deck.pdf"
    
    return {
        "pitch_deck_url": pitch_deck_url,
        "slides": slides,
        "financial_model": financial_model,
        "investor_notes": investor_notes,
        "presentation_script": presentation_script,
        "next_steps": next_steps
    }

def create_pitch_deck_slides(
    business_name: str,
    industry: str,
    business_idea: str,
    problem_statement: str,
    solution: str,
    target_market: str,
    business_model: str,
    funding_amount: float,
    team_info: List[Dict[str, str]],
    competitive_advantage: Optional[str] = None,
    traction: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Create comprehensive pitch deck slides"""
    
    slides = []
    
    # Slide 1: Title Slide
    slides.append({
        "slide_number": 1,
        "title": "Title Slide",
        "content": {
            "company_name": business_name,
            "tagline": f"Transforming {industry} with {business_idea}",
            "presenter": team_info[0]["name"] if team_info else "Founder",
            "date": "2024",
            "contact": "hello@example.com"
        },
        "visual_elements": ["company_logo", "hero_image", "contact_info"]
    })
    
    # Slide 2: Problem Statement
    slides.append({
        "slide_number": 2,
        "title": "The Problem",
        "content": {
            "problem_statement": problem_statement,
            "pain_points": [
                f"Current {industry} solutions are outdated",
                "High costs and complexity",
                "Poor user experience",
                "Lack of innovation"
            ],
            "market_size": f"${get_market_size(industry)}B market opportunity"
        },
        "visual_elements": ["problem_illustration", "market_size_chart"]
    })
    
    # Slide 3: Solution
    slides.append({
        "slide_number": 3,
        "title": "Our Solution",
        "content": {
            "solution_description": solution,
            "key_features": [
                "Innovative technology",
                "User-friendly interface",
                "Cost-effective solution",
                "Scalable platform"
            ],
            "value_proposition": f"Revolutionizing {industry} with {business_idea}"
        },
        "visual_elements": ["solution_diagram", "product_screenshots"]
    })
    
    # Slide 4: Market Opportunity
    slides.append({
        "slide_number": 4,
        "title": "Market Opportunity",
        "content": {
            "total_addressable_market": f"${get_tam(industry)}B",
            "serviceable_addressable_market": f"${get_sam(industry)}B",
            "serviceable_obtainable_market": f"${get_som(industry)}M",
            "target_market": target_market,
            "growth_rate": "15% annually"
        },
        "visual_elements": ["tam_sam_som_chart", "market_growth_graph"]
    })
    
    # Slide 5: Business Model
    slides.append({
        "slide_number": 5,
        "title": "Business Model",
        "content": {
            "revenue_streams": [
                "Subscription fees",
                "Transaction fees",
                "Premium features",
                "Enterprise licensing"
            ],
            "pricing_strategy": "Freemium with premium tiers",
            "customer_acquisition": "Digital marketing + partnerships",
            "unit_economics": {
                "customer_acquisition_cost": "$50",
                "lifetime_value": "$500",
                "payback_period": "6 months"
            }
        },
        "visual_elements": ["revenue_model_diagram", "pricing_table"]
    })
    
    # Slide 6: Traction
    slides.append({
        "slide_number": 6,
        "title": "Traction",
        "content": {
            "key_metrics": traction or {
                "users": "10,000+",
                "revenue": "$50K MRR",
                "growth": "20% MoM",
                "customers": "500+"
            },
            "milestones": [
                "Product launched",
                "First paying customers",
                "Series A ready",
                "Expansion planned"
            ],
            "partnerships": ["Key industry partners", "Strategic alliances"]
        },
        "visual_elements": ["traction_charts", "milestone_timeline"]
    })
    
    # Slide 7: Competition
    slides.append({
        "slide_number": 7,
        "title": "Competitive Landscape",
        "content": {
            "competitors": [
                {"name": "Competitor A", "strength": "Market leader", "weakness": "Outdated tech"},
                {"name": "Competitor B", "strength": "Strong brand", "weakness": "High prices"},
                {"name": "Competitor C", "strength": "Good features", "weakness": "Poor UX"}
            ],
            "competitive_advantage": competitive_advantage or "Superior technology and user experience",
            "differentiation": [
                "Better user interface",
                "Lower costs",
                "Faster implementation",
                "Better customer support"
            ]
        },
        "visual_elements": ["competitive_matrix", "positioning_map"]
    })
    
    # Slide 8: Team
    slides.append({
        "slide_number": 8,
        "title": "Team",
        "content": {
            "team_members": team_info or [
                {"name": "John Doe", "role": "CEO", "background": "Former tech executive"},
                {"name": "Jane Smith", "role": "CTO", "background": "Ex-Google engineer"},
                {"name": "Bob Johnson", "role": "COO", "background": "Operations expert"}
            ],
            "advisors": [
                {"name": "Advisor 1", "role": "Industry expert", "company": "Big Corp"},
                {"name": "Advisor 2", "role": "Investor", "company": "VC Firm"}
            ],
            "hiring_plan": "Key hires in next 6 months"
        },
        "visual_elements": ["team_photos", "org_chart"]
    })
    
    # Slide 9: Financial Projections
    slides.append({
        "slide_number": 9,
        "title": "Financial Projections",
        "content": {
            "revenue_projections": {
                "year_1": "$500K",
                "year_2": "$2M",
                "year_3": "$8M"
            },
            "key_metrics": {
                "gross_margin": "80%",
                "customer_acquisition_cost": "$50",
                "lifetime_value": "$500"
            },
            "funding_requirements": f"${funding_amount:,.0f} for 18 months"
        },
        "visual_elements": ["revenue_chart", "metrics_dashboard"]
    })
    
    # Slide 10: Ask
    slides.append({
        "slide_number": 10,
        "title": "The Ask",
        "content": {
            "funding_amount": f"${funding_amount:,.0f}",
            "use_of_funds": [
                "Product development (40%)",
                "Marketing and sales (30%)",
                "Team expansion (20%)",
                "Operations (10%)"
            ],
            "milestones": [
                "Scale to 100K users",
                "Launch enterprise product",
                "Expand to new markets",
                "Prepare for Series B"
            ],
            "timeline": "18 months runway"
        },
        "visual_elements": ["funding_breakdown", "milestone_timeline"]
    })
    
    return slides

def create_financial_model(
    business_model: str,
    funding_amount: float,
    financial_projections: Optional[Dict[str, Any]] = None,
    industry: str = "technology"
) -> Dict[str, Any]:
    """Create comprehensive financial model"""
    
    # Base projections if not provided
    if not financial_projections:
        financial_projections = {
            "year_1": {"revenue": 500000, "expenses": 800000, "users": 10000},
            "year_2": {"revenue": 2000000, "expenses": 1500000, "users": 50000},
            "year_3": {"revenue": 8000000, "expenses": 4000000, "users": 200000}
        }
    
    # Calculate key metrics
    year_1 = financial_projections["year_1"]
    year_2 = financial_projections["year_2"]
    year_3 = financial_projections["year_3"]
    
    financial_model = {
        "revenue_projections": {
            "year_1": year_1["revenue"],
            "year_2": year_2["revenue"],
            "year_3": year_3["revenue"],
            "growth_rate": ((year_2["revenue"] - year_1["revenue"]) / year_1["revenue"]) * 100
        },
        "expense_breakdown": {
            "personnel": int(funding_amount * 0.4),
            "marketing": int(funding_amount * 0.3),
            "operations": int(funding_amount * 0.2),
            "other": int(funding_amount * 0.1)
        },
        "key_metrics": {
            "customer_acquisition_cost": 50,
            "lifetime_value": 500,
            "gross_margin": 0.8,
            "burn_rate": int(funding_amount / 18),  # 18 months runway
            "months_to_profitability": 24
        },
        "sensitivity_analysis": {
            "conservative": {
                "revenue_multiplier": 0.7,
                "expense_multiplier": 1.2
            },
            "optimistic": {
                "revenue_multiplier": 1.5,
                "expense_multiplier": 0.8
            }
        },
        "funding_requirements": {
            "total_needed": funding_amount,
            "runway_months": 18,
            "next_funding_round": "Series A in 18 months"
        }
    }
    
    return financial_model

def create_investor_notes(
    business_name: str,
    industry: str,
    funding_amount: float,
    team_info: List[Dict[str, str]],
    traction: Optional[Dict[str, Any]] = None
) -> List[str]:
    """Create investor notes and insights"""
    
    notes = [
        f"{business_name} is positioned in the high-growth {industry} sector",
        f"Seeking ${funding_amount:,.0f} to scale operations and expand market reach",
        "Strong founding team with relevant industry experience",
        "Clear path to profitability within 24 months",
        "Large addressable market with significant growth potential",
        "Differentiated product offering with competitive advantages",
        "Proven traction with early customers and revenue",
        "Scalable business model with multiple revenue streams"
    ]
    
    if traction:
        notes.append(f"Strong traction metrics: {traction}")
    
    if team_info:
        notes.append(f"Experienced team with {len(team_info)} key members")
    
    return notes

def create_presentation_script(slides: List[Dict[str, Any]], business_name: str) -> List[Dict[str, Any]]:
    """Create presentation script for each slide"""
    
    script = []
    
    for slide in slides:
        slide_script = {
            "slide_number": slide["slide_number"],
            "title": slide["title"],
            "speaking_notes": f"Present {slide['title']} with confidence and enthusiasm",
            "key_points": [
                f"Focus on the main message of {slide['title']}",
                "Use data and metrics to support your points",
                "Engage the audience with questions",
                "Keep it concise and impactful"
            ],
            "timing": "2-3 minutes per slide",
            "transitions": f"Now let's move to {slide['title']}"
        }
        script.append(slide_script)
    
    return script

def create_next_steps(funding_amount: float, industry: str) -> List[str]:
    """Create next steps for the pitch process"""
    
    return [
        "Schedule meetings with potential investors",
        "Prepare detailed financial model and projections",
        "Conduct due diligence on key metrics",
        "Develop investor presentation materials",
        "Identify and approach target investors",
        "Prepare for investor Q&A sessions",
        "Follow up with interested parties",
        "Negotiate terms and close funding round"
    ]

def get_market_size(industry: str) -> str:
    """Get market size for industry"""
    sizes = {
        "technology": "500",
        "healthcare": "300",
        "finance": "200",
        "ecommerce": "150",
        "education": "100"
    }
    return sizes.get(industry.lower(), "100")

def get_tam(industry: str) -> str:
    """Get Total Addressable Market"""
    tam_values = {
        "technology": "500",
        "healthcare": "300",
        "finance": "200",
        "ecommerce": "150",
        "education": "100"
    }
    return tam_values.get(industry.lower(), "100")

def get_sam(industry: str) -> str:
    """Get Serviceable Addressable Market"""
    return str(int(get_tam(industry)) // 10)

def get_som(industry: str) -> str:
    """Get Serviceable Obtainable Market"""
    return str(int(get_sam(industry)) // 10)

@PITCH_DECK_AGENT.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    ctx.logger.info("Pitch Deck Agent started")
    ctx.logger.info(f"Agent address: {PITCH_DECK_AGENT.address}")

if __name__ == "__main__":
    fund_agent_if_low(PITCH_DECK_AGENT.wallet.address())
    PITCH_DECK_AGENT.run()
