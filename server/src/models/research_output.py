from pydantic import BaseModel, Field 
from typing import List, Optional 
from datetime import datetime

class BusinessIdeaInput(BaseModel): # User input 
    idea: str = Field(..., min_length=10, description="Business idea to research")

class TargetCustomerProfile(BaseModel): 
    demographics: str = Field( ..., description="Comprehensive demographic analysis including age ranges, gender distribution, income levels, geographic location, education, professional background, family status, and household composition. Should include specific data points and market segments." ) 
    psychographics: str = Field( ..., description="Deep psychographic analysis covering core values, beliefs, lifestyle patterns, interests, hobbies, technology adoption, shopping habits, communication styles, aspirations, life goals, pain points, frustrations, and emotional triggers that drive consumer behavior." ) 
    buying_motivators: str = Field( ..., description="Detailed analysis of buying behavior including decision-making process, timeline, key influencers, recommendation sources, price sensitivity, value perception, brand loyalty patterns, channel preferences, purchase frequency, and post-purchase behavior that explains why customers choose one brand over another." )

class MarketPositioning(BaseModel): 
    landscape_summary: str = Field( ..., description="Comprehensive market landscape analysis including market size (TAM/SAM/SOM), growth rates, key trends, competitive landscape overview, market leaders and challengers, industry benchmarks, success factors, barriers to entry, market gaps, emerging opportunities, and strategic market insights." ) 
    unique_value_proposition: str = Field( ..., description="Clear, compelling unique value proposition that differentiates the startup from competitors, including key benefits, features, competitive advantages, positioning strategy, and why customers should choose this solution over alternatives." ) 
    recommended_tone_style: str = Field( ..., description="Specific brand personality and communication recommendations including tone of voice, visual identity direction, messaging approach, communication style, brand personality traits, and how the brand should present itself to resonate with target customers." )

"""Concise branding protocol for design agents""" 
class BrandingProtocol(BaseModel): 
    visual_identity: str = Field( ..., description="Visual design recommendations including colors, typography, imagery style, and logo principles that align with target audience and market positioning." ) 
    tone_voice: str = Field( ..., description="Brand personality, tone of voice, key messages, and communication style recommendations." ) 
    cultural_guidelines: str = Field( ..., description="Cultural considerations, do's and don'ts, regional preferences, and sensitivities to avoid." ) 
    competitive_differentiation: str = Field( ..., description="What makes the brand unique, positioning opportunities, and elements to avoid (competitor overlaps)." )

class MarketResearchOutput(BaseModel): 
    business_idea: str 
    target_customer_profile: TargetCustomerProfile 
    market_positioning: MarketPositioning 
    branding_protocol: BrandingProtocol 
    timestamp: datetime

if __name__ == "__main__": 
    print("Hello World")