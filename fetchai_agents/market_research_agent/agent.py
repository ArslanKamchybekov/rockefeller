"""
Market Research Agent for Fetch.ai AgentVerse
Finds trending niches and product demand analysis
"""

from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from pydantic import BaseModel
import requests
import json
import os
from typing import List, Dict, Any
import asyncio

# Agent configuration
MARKET_RESEARCH_AGENT = Agent(
    name="market_research_agent",
    seed="market-research-agent-seed-phrase-12345",
    port=8001,
    endpoint=["http://localhost:8001/submit"],
)

# Pydantic models for type safety
class MarketResearchRequest(BaseModel):
    industry: str
    region: str = "global"
    focus_areas: List[str] = ["trends", "competitors", "demand", "pricing"]
    budget_range: str = "any"

class MarketResearchResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    trending_products: List[Dict[str, Any]]
    competitor_analysis: Dict[str, Any]
    market_size: Dict[str, Any]

class ErrorResponse(BaseModel):
    success: bool
    error: str

@MARKET_RESEARCH_AGENT.on_message(model=MarketResearchRequest)
async def handle_market_research_request(ctx: Context, sender: str, msg: MarketResearchRequest):
    """Handle market research requests"""
    try:
        ctx.logger.info(f"Received market research request for {msg.industry} in {msg.region}")
        
        # Perform market research
        research_data = await perform_market_research(
            industry=msg.industry,
            region=msg.region,
            focus_areas=msg.focus_areas,
            budget_range=msg.budget_range
        )
        
        response = MarketResearchResponse(
            success=True,
            data=research_data,
            insights=research_data.get("insights", []),
            recommendations=research_data.get("recommendations", []),
            trending_products=research_data.get("trending_products", []),
            competitor_analysis=research_data.get("competitor_analysis", {}),
            market_size=research_data.get("market_size", {})
        )
        
        await ctx.send(sender, response.model_dump())
        ctx.logger.info(f"Sent market research response to {sender}")
        
    except Exception as e:
        ctx.logger.error(f"Error in market research: {e}")
        error_response = ErrorResponse(success=False, error=str(e))
        await ctx.send(sender, error_response.model_dump())

async def perform_market_research(industry: str, region: str, focus_areas: List[str], budget_range: str) -> Dict[str, Any]:
    """Perform comprehensive market research"""
    
    # Simulate market research data (replace with real API calls)
    research_data = {
        "industry": industry,
        "region": region,
        "focus_areas": focus_areas,
        "budget_range": budget_range,
        "insights": [
            f"Growing demand in {industry} sector with 15% YoY growth",
            f"Key trend: Sustainability focus in {region} market",
            f"Emerging opportunities in digital transformation",
            f"Consumer behavior shift towards online purchasing"
        ],
        "recommendations": [
            "Focus on sustainable product offerings",
            "Invest in digital marketing channels",
            "Target Gen Z and Millennial demographics",
            "Consider subscription-based business models"
        ],
        "trending_products": [
            {
                "name": f"Eco-friendly {industry} products",
                "demand_score": 8.5,
                "competition_level": "medium",
                "profit_margin": "high"
            },
            {
                "name": f"AI-powered {industry} solutions",
                "demand_score": 9.2,
                "competition_level": "low",
                "profit_margin": "very_high"
            }
        ],
        "competitor_analysis": {
            "top_competitors": [
                {"name": f"Leading {industry} Company A", "market_share": "25%", "strengths": ["Brand recognition", "Distribution network"]},
                {"name": f"Emerging {industry} Company B", "market_share": "15%", "strengths": ["Innovation", "Customer service"]}
            ],
            "market_gaps": [
                "Lack of personalized customer experience",
                "Limited mobile-first solutions",
                "Insufficient sustainability focus"
            ]
        },
        "market_size": {
            "total_addressable_market": f"$2.5B in {region}",
            "serviceable_addressable_market": f"$500M in {region}",
            "serviceable_obtainable_market": f"$50M in {region}",
            "growth_rate": "12% annually"
        }
    }
    
    return research_data

@MARKET_RESEARCH_AGENT.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    ctx.logger.info("Market Research Agent started")
    ctx.logger.info(f"Agent address: {MARKET_RESEARCH_AGENT.address}")

if __name__ == "__main__":
    fund_agent_if_low(MARKET_RESEARCH_AGENT.wallet.address())
    MARKET_RESEARCH_AGENT.run()
