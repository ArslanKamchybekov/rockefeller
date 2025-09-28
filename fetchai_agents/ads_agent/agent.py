"""
Ads Agent for Fetch.ai AgentVerse
Launches Google and Meta advertising campaigns instantly
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
ADS_AGENT = Agent(
    name="ads_agent",
    seed="ads-agent-seed-phrase-12345",
    port=8004,
    endpoint=["http://localhost:8004/submit"],
)

# Pydantic models
class AdsCampaignRequest(BaseModel):
    business_name: str
    industry: str
    target_audience: Dict[str, Any]
    budget: float
    duration_days: int
    platforms: List[str] = ["google", "meta"]
    campaign_type: str = "awareness"  # awareness, conversion, traffic
    products: List[Dict[str, Any]] = []
    brand_assets: Optional[Dict[str, str]] = None

class AdsCampaignResponse(BaseModel):
    success: bool
    campaign_id: str
    platforms_launched: List[str]
    budget_allocation: Dict[str, float]
    ad_creatives: List[Dict[str, Any]]
    targeting_summary: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    optimization_recommendations: List[str]

class ErrorResponse(BaseModel):
    success: bool
    error: str

@ADS_AGENT.on_message(model=AdsCampaignRequest)
async def handle_ads_request(ctx: Context, sender: str, msg: AdsCampaignRequest):
    """Handle advertising campaign requests"""
    try:
        ctx.logger.info(f"Received ads campaign request for {msg.business_name}")
        
        # Launch advertising campaigns
        campaign_data = await launch_advertising_campaigns(
            business_name=msg.business_name,
            industry=msg.industry,
            target_audience=msg.target_audience,
            budget=msg.budget,
            duration_days=msg.duration_days,
            platforms=msg.platforms,
            campaign_type=msg.campaign_type,
            products=msg.products,
            brand_assets=msg.brand_assets
        )
        
        response = AdsCampaignResponse(
            success=True,
            campaign_id=campaign_data["campaign_id"],
            platforms_launched=campaign_data["platforms_launched"],
            budget_allocation=campaign_data["budget_allocation"],
            ad_creatives=campaign_data["ad_creatives"],
            targeting_summary=campaign_data["targeting_summary"],
            performance_metrics=campaign_data["performance_metrics"],
            optimization_recommendations=campaign_data["optimization_recommendations"]
        )
        
        await ctx.send(sender, response.model_dump())
        ctx.logger.info(f"Sent ads campaign response to {sender}")
        
    except Exception as e:
        ctx.logger.error(f"Error in ads campaign creation: {e}")
        error_response = ErrorResponse(success=False, error=str(e))
        await ctx.send(sender, error_response.model_dump())

async def launch_advertising_campaigns(
    business_name: str,
    industry: str,
    target_audience: Dict[str, Any],
    budget: float,
    duration_days: int,
    platforms: List[str],
    campaign_type: str,
    products: List[Dict[str, Any]],
    brand_assets: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Launch advertising campaigns across multiple platforms"""
    
    campaign_id = f"campaign_{hash(business_name) % 1000000}"
    
    # Allocate budget across platforms
    budget_allocation = allocate_budget(budget, platforms)
    
    # Create ad creatives
    ad_creatives = create_ad_creatives(business_name, industry, products, brand_assets)
    
    # Configure targeting
    targeting_summary = configure_targeting(target_audience, industry)
    
    # Launch campaigns on each platform
    platforms_launched = []
    for platform in platforms:
        if platform.lower() == "google":
            platforms_launched.append(launch_google_campaign(campaign_id, budget_allocation[platform]))
        elif platform.lower() == "meta":
            platforms_launched.append(launch_meta_campaign(campaign_id, budget_allocation[platform]))
    
    # Generate performance metrics
    performance_metrics = generate_performance_metrics(campaign_type, budget, duration_days)
    
    # Generate optimization recommendations
    optimization_recommendations = generate_optimization_recommendations(
        industry, campaign_type, target_audience, budget
    )
    
    return {
        "campaign_id": campaign_id,
        "platforms_launched": platforms_launched,
        "budget_allocation": budget_allocation,
        "ad_creatives": ad_creatives,
        "targeting_summary": targeting_summary,
        "performance_metrics": performance_metrics,
        "optimization_recommendations": optimization_recommendations
    }

def allocate_budget(total_budget: float, platforms: List[str]) -> Dict[str, float]:
    """Allocate budget across advertising platforms"""
    if len(platforms) == 1:
        return {platforms[0]: total_budget}
    
    # Default allocation: 60% Google, 40% Meta
    allocation = {}
    if "google" in platforms and "meta" in platforms:
        allocation["google"] = total_budget * 0.6
        allocation["meta"] = total_budget * 0.4
    else:
        per_platform = total_budget / len(platforms)
        for platform in platforms:
            allocation[platform] = per_platform
    
    return allocation

def create_ad_creatives(
    business_name: str,
    industry: str,
    products: List[Dict[str, Any]],
    brand_assets: Optional[Dict[str, str]] = None
) -> List[Dict[str, Any]]:
    """Create ad creatives for different platforms"""
    
    creatives = []
    
    # Google Ads creatives
    google_creatives = {
        "headlines": [
            f"Shop {business_name} - Premium {industry}",
            f"Discover {business_name} Collection",
            f"Quality {industry} at {business_name}"
        ],
        "descriptions": [
            f"Find the best {industry} products at {business_name}. Quality guaranteed, fast shipping.",
            f"Shop {business_name} for premium {industry} solutions. Trusted by thousands.",
            f"Your one-stop shop for {industry}. {business_name} has everything you need."
        ],
        "call_to_action": ["Shop Now", "Learn More", "Get Started"]
    }
    
    # Meta Ads creatives
    meta_creatives = {
        "primary_text": f"Discover {business_name} - Your premier {industry} destination. Quality products, exceptional service.",
        "headlines": [
            f"Shop {business_name}",
            f"Premium {industry}",
            f"Quality Guaranteed"
        ],
        "descriptions": f"Find everything you need for {industry} at {business_name}. Fast shipping, great prices.",
        "call_to_action": "Shop Now"
    }
    
    creatives.extend([
        {
            "platform": "google",
            "type": "search_ad",
            "content": google_creatives,
            "status": "active"
        },
        {
            "platform": "meta",
            "type": "feed_ad",
            "content": meta_creatives,
            "status": "active"
        }
    ])
    
    return creatives

def configure_targeting(target_audience: Dict[str, Any], industry: str) -> Dict[str, Any]:
    """Configure targeting parameters"""
    return {
        "demographics": {
            "age_range": target_audience.get("age_range", "25-54"),
            "gender": target_audience.get("gender", "all"),
            "income": target_audience.get("income", "middle_high")
        },
        "interests": target_audience.get("interests", [industry, "shopping", "lifestyle"]),
        "behaviors": target_audience.get("behaviors", ["online_shoppers", "brand_conscious"]),
        "locations": target_audience.get("locations", ["United States"]),
        "devices": target_audience.get("devices", ["mobile", "desktop"])
    }

def launch_google_campaign(campaign_id: str, budget: float) -> str:
    """Launch Google Ads campaign"""
    # Simulate Google Ads API call
    return f"google_campaign_{campaign_id}"

def launch_meta_campaign(campaign_id: str, budget: float) -> str:
    """Launch Meta Ads campaign"""
    # Simulate Meta Ads API call
    return f"meta_campaign_{campaign_id}"

def generate_performance_metrics(campaign_type: str, budget: float, duration_days: int) -> Dict[str, Any]:
    """Generate expected performance metrics"""
    base_metrics = {
        "impressions": int(budget * 1000),  # Estimated impressions
        "clicks": int(budget * 50),  # Estimated clicks
        "conversions": int(budget * 5),  # Estimated conversions
        "cost_per_click": budget / 50,
        "click_through_rate": 0.05,  # 5% CTR
        "conversion_rate": 0.10,  # 10% conversion rate
        "return_on_ad_spend": 3.0  # 3x ROAS
    }
    
    if campaign_type == "awareness":
        base_metrics["reach"] = int(budget * 2000)
        base_metrics["frequency"] = 2.5
    elif campaign_type == "conversion":
        base_metrics["cost_per_conversion"] = budget / 5
        base_metrics["conversion_value"] = budget * 3
    
    return base_metrics

def generate_optimization_recommendations(
    industry: str,
    campaign_type: str,
    target_audience: Dict[str, Any],
    budget: float
) -> List[str]:
    """Generate optimization recommendations"""
    recommendations = [
        "Monitor campaign performance daily for the first week",
        "A/B test different ad creatives to find top performers",
        "Adjust bids based on time of day performance",
        "Expand targeting to similar audiences after initial success",
        "Create lookalike audiences from your best customers"
    ]
    
    if budget > 1000:
        recommendations.append("Consider video ads for higher engagement")
    
    if campaign_type == "conversion":
        recommendations.append("Set up conversion tracking and attribution")
    
    return recommendations

@ADS_AGENT.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    ctx.logger.info("Ads Agent started")
    ctx.logger.info(f"Agent address: {ADS_AGENT.address}")

if __name__ == "__main__":
    fund_agent_if_low(ADS_AGENT.wallet.address())
    ADS_AGENT.run()
