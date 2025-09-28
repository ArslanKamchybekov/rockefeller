"""
Influencer Agent for Fetch.ai AgentVerse
Finds and drafts outreach to micro-influencers
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
INFLUENCER_AGENT = Agent(
    name="influencer_agent",
    seed="influencer-agent-seed-phrase-12345",
    port=8007,
    endpoint=["http://localhost:8007/submit"],
)

# Pydantic models
class InfluencerRequest(BaseModel):
    business_name: str
    industry: str
    target_audience: Dict[str, Any]
    budget_range: str = "1000-5000"
    campaign_goals: List[str] = ["brand_awareness", "engagement", "sales"]
    content_types: List[str] = ["posts", "stories", "reels"]
    platforms: List[str] = ["instagram", "tiktok", "youtube"]
    brand_values: List[str] = ["authenticity", "quality", "innovation"]

class InfluencerResponse(BaseModel):
    success: bool
    influencers_found: List[Dict[str, Any]]
    outreach_templates: List[Dict[str, Any]]
    campaign_strategy: Dict[str, Any]
    budget_allocation: Dict[str, Any]
    content_briefs: List[Dict[str, Any]]
    performance_metrics: Dict[str, Any]

class ErrorResponse(BaseModel):
    success: bool
    error: str

@INFLUENCER_AGENT.on_message(model=InfluencerRequest)
async def handle_influencer_request(ctx: Context, sender: str, msg: InfluencerRequest):
    """Handle influencer marketing requests"""
    try:
        ctx.logger.info(f"Received influencer request for {msg.business_name}")
        
        # Find influencers and create outreach strategy
        influencer_data = await find_influencers_and_create_strategy(
            business_name=msg.business_name,
            industry=msg.industry,
            target_audience=msg.target_audience,
            budget_range=msg.budget_range,
            campaign_goals=msg.campaign_goals,
            content_types=msg.content_types,
            platforms=msg.platforms,
            brand_values=msg.brand_values
        )
        
        response = InfluencerResponse(
            success=True,
            influencers_found=influencer_data["influencers_found"],
            outreach_templates=influencer_data["outreach_templates"],
            campaign_strategy=influencer_data["campaign_strategy"],
            budget_allocation=influencer_data["budget_allocation"],
            content_briefs=influencer_data["content_briefs"],
            performance_metrics=influencer_data["performance_metrics"]
        )
        
        await ctx.send(sender, response.model_dump())
        ctx.logger.info(f"Sent influencer response to {sender}")
        
    except Exception as e:
        ctx.logger.error(f"Error in influencer strategy: {e}")
        error_response = ErrorResponse(success=False, error=str(e))
        await ctx.send(sender, error_response.model_dump())

async def find_influencers_and_create_strategy(
    business_name: str,
    industry: str,
    target_audience: Dict[str, Any],
    budget_range: str,
    campaign_goals: List[str],
    content_types: List[str],
    platforms: List[str],
    brand_values: List[str]
) -> Dict[str, Any]:
    """Find influencers and create comprehensive outreach strategy"""
    
    # Find relevant influencers
    influencers_found = find_relevant_influencers(
        industry, target_audience, platforms, budget_range
    )
    
    # Create outreach templates
    outreach_templates = create_outreach_templates(
        business_name, industry, brand_values, campaign_goals
    )
    
    # Develop campaign strategy
    campaign_strategy = develop_campaign_strategy(
        business_name, industry, campaign_goals, content_types, platforms
    )
    
    # Allocate budget
    budget_allocation = allocate_influencer_budget(
        budget_range, influencers_found, platforms
    )
    
    # Create content briefs
    content_briefs = create_content_briefs(
        business_name, industry, content_types, brand_values
    )
    
    # Generate performance metrics
    performance_metrics = generate_influencer_metrics(
        campaign_goals, platforms, budget_range
    )
    
    return {
        "influencers_found": influencers_found,
        "outreach_templates": outreach_templates,
        "campaign_strategy": campaign_strategy,
        "budget_allocation": budget_allocation,
        "content_briefs": content_briefs,
        "performance_metrics": performance_metrics
    }

def find_relevant_influencers(
    industry: str,
    target_audience: Dict[str, Any],
    platforms: List[str],
    budget_range: str
) -> List[Dict[str, Any]]:
    """Find relevant micro-influencers for the campaign"""
    
    # Simulate influencer database search
    influencers = []
    
    # Micro-influencers (1K-10K followers)
    micro_influencers = [
        {
            "name": "Sarah Chen",
            "handle": "@sarahchen_lifestyle",
            "platform": "instagram",
            "followers": 8500,
            "engagement_rate": 4.2,
            "niche": "lifestyle",
            "location": "Los Angeles, CA",
            "rate_range": "$200-500",
            "contact_email": "sarah@example.com",
            "bio": "Lifestyle blogger sharing daily inspiration",
            "brand_affinity": 0.8,
            "audience_demographics": {
                "age_range": "25-34",
                "gender": "70% female",
                "interests": ["fashion", "beauty", "wellness"]
            }
        },
        {
            "name": "Mike Rodriguez",
            "handle": "@mike_techreviews",
            "platform": "youtube",
            "followers": 12000,
            "engagement_rate": 3.8,
            "niche": "technology",
            "location": "Austin, TX",
            "rate_range": "$300-600",
            "contact_email": "mike@example.com",
            "bio": "Tech enthusiast reviewing gadgets and apps",
            "brand_affinity": 0.7,
            "audience_demographics": {
                "age_range": "18-35",
                "gender": "60% male",
                "interests": ["technology", "gaming", "startups"]
            }
        }
    ]
    
    # Mid-tier influencers (10K-100K followers)
    mid_tier_influencers = [
        {
            "name": "Emma Thompson",
            "handle": "@emma_wellness",
            "platform": "instagram",
            "followers": 45000,
            "engagement_rate": 5.1,
            "niche": "wellness",
            "location": "Portland, OR",
            "rate_range": "$800-1500",
            "contact_email": "emma@example.com",
            "bio": "Wellness coach and fitness enthusiast",
            "brand_affinity": 0.9,
            "audience_demographics": {
                "age_range": "25-45",
                "gender": "85% female",
                "interests": ["fitness", "nutrition", "mental_health"]
            }
        },
        {
            "name": "David Park",
            "handle": "@david_entrepreneur",
            "platform": "linkedin",
            "followers": 25000,
            "engagement_rate": 6.2,
            "niche": "business",
            "location": "New York, NY",
            "rate_range": "$1000-2000",
            "contact_email": "david@example.com",
            "bio": "Serial entrepreneur sharing business insights",
            "brand_affinity": 0.8,
            "audience_demographics": {
                "age_range": "28-50",
                "gender": "60% male",
                "interests": ["entrepreneurship", "startups", "investing"]
            }
        }
    ]
    
    # Filter based on budget range
    if "1000-5000" in budget_range:
        influencers.extend(micro_influencers)
        influencers.extend(mid_tier_influencers[:1])
    elif "500-2000" in budget_range:
        influencers.extend(micro_influencers)
    else:
        influencers.extend(micro_influencers[:1])
    
    return influencers

def create_outreach_templates(
    business_name: str,
    industry: str,
    brand_values: List[str],
    campaign_goals: List[str]
) -> List[Dict[str, Any]]:
    """Create personalized outreach templates"""
    
    templates = []
    
    # Initial outreach template
    initial_template = {
        "type": "initial_outreach",
        "subject": f"Partnership Opportunity with {business_name}",
        "content": f"""
Hi [INFLUENCER_NAME],

I hope this message finds you well! I'm reaching out from {business_name}, a growing company in the {industry} space.

I've been following your content on [PLATFORM] and I'm impressed by your authentic voice and engaged community. Your posts about [RELEVANT_TOPIC] really resonate with our brand values of {', '.join(brand_values)}.

We're looking to partner with creators who share our vision and would love to collaborate with you on a campaign focused on {', '.join(campaign_goals)}.

Here's what we're offering:
• Competitive compensation: [RATE_RANGE]
• Creative freedom within brand guidelines
• Long-term partnership opportunities
• Product samples and exclusive access

Would you be interested in a brief call to discuss this opportunity? I'd love to learn more about your content strategy and how we can work together.

Best regards,
[YOUR_NAME]
{business_name} Marketing Team
        """,
        "placeholders": ["[INFLUENCER_NAME]", "[PLATFORM]", "[RELEVANT_TOPIC]", "[RATE_RANGE]", "[YOUR_NAME]"],
        "personalization_tips": [
            "Mention specific posts they've made",
            "Reference their recent content themes",
            "Include their follower count and engagement rate"
        ]
    }
    
    # Follow-up template
    followup_template = {
        "type": "follow_up",
        "subject": f"Following up on {business_name} Partnership",
        "content": f"""
Hi [INFLUENCER_NAME],

I wanted to follow up on my previous message about the partnership opportunity with {business_name}.

I understand you're busy, but I believe this collaboration could be mutually beneficial. We're offering:

• [SPECIFIC_RATE] for [CONTENT_TYPE]
• [TIMELINE] for content delivery
• [CREATIVE_GUIDELINES] for brand alignment

I'd love to schedule a quick 15-minute call to discuss the details. Would [SUGGESTED_TIME] work for you?

If you're not interested, no worries at all! Just let me know and I'll remove you from our outreach list.

Best regards,
[YOUR_NAME]
        """,
        "placeholders": ["[INFLUENCER_NAME]", "[SPECIFIC_RATE]", "[CONTENT_TYPE]", "[TIMELINE]", "[CREATIVE_GUIDELINES]", "[SUGGESTED_TIME]", "[YOUR_NAME]"],
        "personalization_tips": [
            "Reference the specific rate discussed",
            "Mention the content type they're interested in",
            "Suggest specific times based on their timezone"
        ]
    }
    
    # Collaboration agreement template
    agreement_template = {
        "type": "collaboration_agreement",
        "subject": f"Partnership Agreement - {business_name}",
        "content": f"""
Hi [INFLUENCER_NAME],

Thank you for your interest in partnering with {business_name}! I'm excited to work together.

Here are the collaboration details:

**Campaign Overview:**
• Brand: {business_name}
• Content Type: [CONTENT_TYPE]
• Platform: [PLATFORM]
• Timeline: [TIMELINE]
• Compensation: [COMPENSATION]

**Deliverables:**
• [NUMBER_OF_POSTS] posts featuring our product
• [STORY_REQUIREMENTS] stories
• [HASHTAG_REQUIREMENTS] hashtags
• [TAG_REQUIREMENTS] brand tags

**Creative Guidelines:**
• Maintain your authentic voice
• Include [KEY_MESSAGING]
• Use [BRAND_HASHTAGS]
• Tag @{business_name.lower().replace(' ', '')}

**Timeline:**
• Content creation: [CREATION_PERIOD]
• Review period: [REVIEW_PERIOD]
• Posting schedule: [POSTING_SCHEDULE]

Please confirm your acceptance of these terms, and I'll send over the formal agreement.

Looking forward to working with you!

Best regards,
[YOUR_NAME]
        """,
        "placeholders": ["[INFLUENCER_NAME]", "[CONTENT_TYPE]", "[PLATFORM]", "[TIMELINE]", "[COMPENSATION]", "[NUMBER_OF_POSTS]", "[STORY_REQUIREMENTS]", "[HASHTAG_REQUIREMENTS]", "[TAG_REQUIREMENTS]", "[KEY_MESSAGING]", "[BRAND_HASHTAGS]", "[CREATION_PERIOD]", "[REVIEW_PERIOD]", "[POSTING_SCHEDULE]", "[YOUR_NAME]"],
        "personalization_tips": [
            "Customize based on their preferred content type",
            "Adjust timeline based on their availability",
            "Include specific brand messaging"
        ]
    }
    
    templates.extend([initial_template, followup_template, agreement_template])
    
    return templates

def develop_campaign_strategy(
    business_name: str,
    industry: str,
    campaign_goals: List[str],
    content_types: List[str],
    platforms: List[str]
) -> Dict[str, Any]:
    """Develop comprehensive influencer campaign strategy"""
    
    return {
        "campaign_name": f"{business_name} Influencer Campaign",
        "objectives": campaign_goals,
        "target_audience": {
            "demographics": "18-45 years old",
            "interests": [industry, "lifestyle", "technology"],
            "behavior": "social media active, brand conscious"
        },
        "content_strategy": {
            "content_types": content_types,
            "posting_frequency": "2-3 posts per week",
            "story_requirements": "Daily stories during campaign",
            "hashtag_strategy": f"#{business_name.lower().replace(' ', '')}, #branded, #sponsored"
        },
        "platform_strategy": {
            platform: {
                "content_focus": f"{platform}-specific content",
                "posting_schedule": "Prime time hours",
                "engagement_tactics": "Respond to comments, engage with followers"
            } for platform in platforms
        },
        "timeline": {
            "preparation": "2 weeks",
            "content_creation": "1 week",
            "campaign_duration": "4 weeks",
            "follow_up": "2 weeks"
        },
        "success_metrics": [
            "Reach and impressions",
            "Engagement rate",
            "Click-through rate",
            "Brand mention sentiment",
            "Sales attribution"
        ]
    }

def allocate_influencer_budget(
    budget_range: str,
    influencers: List[Dict[str, Any]],
    platforms: List[str]
) -> Dict[str, Any]:
    """Allocate budget across influencers and platforms"""
    
    # Parse budget range
    if "1000-5000" in budget_range:
        total_budget = 3000  # Use middle of range
    elif "500-2000" in budget_range:
        total_budget = 1250
    else:
        total_budget = 1000
    
    # Allocate to influencers based on their rates and reach
    influencer_allocation = {}
    remaining_budget = total_budget
    
    for influencer in influencers:
        # Calculate allocation based on follower count and engagement
        follower_score = min(influencer["followers"] / 10000, 1)  # Normalize to 0-1
        engagement_score = influencer["engagement_rate"] / 10  # Normalize to 0-1
        allocation_score = (follower_score + engagement_score) / 2
        
        allocation = int(total_budget * allocation_score * 0.3)  # 30% of budget per influencer
        influencer_allocation[influencer["name"]] = allocation
        remaining_budget -= allocation
    
    # Allocate remaining budget to content creation and tools
    content_creation = int(remaining_budget * 0.6)
    tools_and_analytics = int(remaining_budget * 0.4)
    
    return {
        "total_budget": total_budget,
        "influencer_allocation": influencer_allocation,
        "content_creation": content_creation,
        "tools_and_analytics": tools_and_analytics,
        "platform_distribution": {
            platform: int(total_budget * 0.4 / len(platforms)) for platform in platforms
        }
    }

def create_content_briefs(
    business_name: str,
    industry: str,
    content_types: List[str],
    brand_values: List[str]
) -> List[Dict[str, Any]]:
    """Create content briefs for influencers"""
    
    briefs = []
    
    for content_type in content_types:
        brief = {
            "content_type": content_type,
            "title": f"{business_name} {content_type.title()} Brief",
            "objective": f"Create engaging {content_type} content that showcases {business_name}",
            "key_messages": [
                f"{business_name} is a trusted {industry} brand",
                f"Our products deliver {', '.join(brand_values)}",
                "Perfect for your lifestyle and needs"
            ],
            "visual_requirements": {
                "style": "Clean, modern, lifestyle-focused",
                "colors": "Brand colors with natural lighting",
                "mood": "Authentic, aspirational, relatable"
            },
            "copy_requirements": {
                "tone": "Conversational and authentic",
                "hashtags": f"#{business_name.lower().replace(' ', '')} #sponsored #ad",
                "call_to_action": "Visit our website or DM for more info"
            },
            "do_nots": [
                "Don't make false claims about the product",
                "Don't use competitor products in the same post",
                "Don't forget to include required hashtags"
            ],
            "timeline": "Content due 3 days before posting date"
        }
        briefs.append(brief)
    
    return briefs

def generate_influencer_metrics(
    campaign_goals: List[str],
    platforms: List[str],
    budget_range: str
) -> Dict[str, Any]:
    """Generate expected performance metrics"""
    
    base_metrics = {
        "reach": "50,000-100,000",
        "impressions": "150,000-300,000",
        "engagement_rate": "4-6%",
        "click_through_rate": "2-4%",
        "cost_per_engagement": "$0.50-1.50",
        "return_on_investment": "3-5x"
    }
    
    if "brand_awareness" in campaign_goals:
        base_metrics["brand_mention_sentiment"] = "85% positive"
        base_metrics["brand_recall"] = "40-60%"
    
    if "sales" in campaign_goals:
        base_metrics["conversion_rate"] = "2-5%"
        base_metrics["sales_attribution"] = "15-25%"
    
    return base_metrics

@INFLUENCER_AGENT.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    ctx.logger.info("Influencer Agent started")
    ctx.logger.info(f"Agent address: {INFLUENCER_AGENT.address}")

if __name__ == "__main__":
    fund_agent_if_low(INFLUENCER_AGENT.wallet.address())
    INFLUENCER_AGENT.run()
