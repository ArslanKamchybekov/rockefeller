"""
Deployment script for all Fetch.ai agents to AgentVerse
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import json
from dotenv import load_dotenv

# Add the parent directory to the path to import agents
sys.path.append(str(Path(__file__).parent.parent))

try:
    from fetchai.registration import register_with_agentverse
    from uagents_core.identity import Identity
except ImportError:
    print("Error: fetchai package not installed. Run: pip install fetchai")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Agent configurations
AGENTS = [
    {
        "name": "market_research_agent",
        "seed": "market-research-agent-seed-phrase-12345",
        "port": 8001,
        "url": "http://localhost:8001",
        "title": "Market Research Agent",
        "description": "Finds trending niches and analyzes product demand",
        "readme": """
# Market Research Agent

This agent specializes in comprehensive market research and analysis.

## Features
- **Trending Niches Discovery**: Identifies emerging market opportunities
- **Product Demand Analysis**: Analyzes market demand for specific products
- **Competitor Research**: Provides detailed competitor analysis
- **Market Size Estimation**: Calculates TAM, SAM, and SOM
- **Industry Insights**: Delivers actionable market intelligence

## Usage
Send a market research request with:
- Industry or market sector
- Geographic region
- Focus areas (trends, competitors, demand, pricing)
- Budget range

## Output
- Market insights and trends
- Competitor analysis
- Product recommendations
- Market size estimates
- Strategic recommendations

## Perfect for
- Entrepreneurs validating business ideas
- Product managers researching markets
- Investors analyzing opportunities
- Consultants providing market intelligence
        """,
        "tags": ["market-research", "trends", "analysis", "business-intelligence"]
    },
    {
        "name": "branding_agent",
        "seed": "branding-agent-seed-phrase-12345",
        "port": 8002,
        "url": "http://localhost:8002",
        "title": "Branding Agent",
        "description": "Creates logos, taglines, color schemes, and visual assets",
        "readme": """
# Branding Agent

This agent creates comprehensive branding assets for your business.

## Features
- **Brand Name Generation**: Creates memorable and relevant brand names
- **Tagline Creation**: Develops compelling taglines and slogans
- **Color Scheme Design**: Generates cohesive color palettes
- **Logo Concepts**: Provides detailed logo descriptions and concepts
- **Brand Guidelines**: Creates comprehensive brand style guides
- **Visual Assets**: Generates business cards, social media templates

## Usage
Send a branding request with:
- Business idea or concept
- Industry
- Target audience
- Brand personality preferences
- Color preferences (optional)

## Output
- Brand name and tagline
- Complete color scheme
- Logo descriptions
- Brand guidelines
- Visual asset recommendations

## Perfect for
- Startups creating their brand identity
- Businesses rebranding
- Entrepreneurs launching new products
- Designers seeking inspiration
        """,
        "tags": ["branding", "logo", "design", "marketing", "visual-identity"]
    },
    {
        "name": "shopify_agent",
        "seed": "shopify-agent-seed-phrase-12345",
        "port": 8003,
        "url": "http://localhost:8003",
        "title": "Shopify Store Agent",
        "description": "Creates and publishes Shopify storefronts",
        "readme": """
# Shopify Store Agent

This agent helps you create and launch professional Shopify stores.

## Features
- **Store Creation**: Sets up complete Shopify storefronts
- **Theme Selection**: Chooses appropriate themes for your industry
- **Product Management**: Adds and organizes products
- **Payment Setup**: Configures payment methods
- **Shipping Configuration**: Sets up shipping zones and rates
- **Domain Setup**: Helps with custom domain configuration

## Usage
Send a store creation request with:
- Store name
- Industry
- Product information
- Theme preferences
- Payment methods
- Shipping zones

## Output
- Live store URL
- Admin panel access
- Store configuration details
- Next steps checklist

## Perfect for
- E-commerce entrepreneurs
- Dropshipping businesses
- Physical product sellers
- Digital product creators
        """,
        "tags": ["shopify", "ecommerce", "store", "online-selling", "dropshipping"]
    },
    {
        "name": "ads_agent",
        "seed": "ads-agent-seed-phrase-12345",
        "port": 8004,
        "url": "http://localhost:8004",
        "title": "Ads Agent",
        "description": "Launches Google and Meta advertising campaigns",
        "readme": """
# Ads Agent

This agent creates and launches advertising campaigns across multiple platforms.

## Features
- **Multi-Platform Campaigns**: Google Ads and Meta Ads
- **Budget Allocation**: Smart budget distribution across platforms
- **Ad Creative Generation**: Creates compelling ad copy and visuals
- **Targeting Setup**: Configures precise audience targeting
- **Campaign Optimization**: Provides optimization recommendations
- **Performance Tracking**: Monitors campaign metrics

## Usage
Send an ads campaign request with:
- Business name and industry
- Target audience details
- Budget range
- Campaign goals
- Platforms to use

## Output
- Campaign IDs and URLs
- Ad creatives and copy
- Targeting configuration
- Performance metrics
- Optimization recommendations

## Perfect for
- E-commerce businesses
- Service providers
- App developers
- Local businesses
        """,
        "tags": ["advertising", "google-ads", "meta-ads", "marketing", "campaigns"]
    },
    {
        "name": "legal_docs_agent",
        "seed": "legal-docs-agent-seed-phrase-12345",
        "port": 8005,
        "url": "http://localhost:8005",
        "title": "Legal Docs Agent",
        "description": "Auto-generates LLC docs, policies, and Terms of Service",
        "readme": """
# Legal Docs Agent

This agent generates comprehensive legal documents for your business.

## Features
- **LLC Formation**: Complete LLC formation documents
- **Privacy Policies**: GDPR and CCPA compliant privacy policies
- **Terms of Service**: Comprehensive terms and conditions
- **NDA Templates**: Non-disclosure agreement templates
- **Employment Contracts**: Employment agreement templates
- **Compliance Checklists**: Step-by-step compliance guides

## Usage
Send a legal docs request with:
- Business name and type
- Industry
- Business address
- Owner information
- Required document types

## Output
- Generated legal documents
- Filing requirements
- Compliance checklist
- Next steps
- Cost estimates

## Perfect for
- New business owners
- Startups needing legal protection
- Entrepreneurs launching products
- Businesses expanding operations
        """,
        "tags": ["legal", "documents", "compliance", "llc", "privacy-policy"]
    },
    {
        "name": "customer_service_agent",
        "seed": "customer-service-agent-seed-phrase-12345",
        "port": 8006,
        "url": "http://localhost:8006",
        "title": "Customer Service Agent",
        "description": "Drafts email templates and automates customer responses",
        "readme": """
# Customer Service Agent

This agent automates customer service with email templates and phone systems.

## Features
- **Email Templates**: Automated response templates
- **Phone Automation**: VAPI phone assistant setup
- **Chat Responses**: Automated chat responses
- **Ticket Management**: Support ticket automation
- **Performance Metrics**: Customer service analytics
- **Brand Voice**: Consistent brand communication

## Usage
Send a customer service request with:
- Business name and industry
- Service types needed
- Phone number (optional)
- Business hours
- Common issues

## Output
- Email templates
- Phone automation config
- Chat responses
- VAPI setup
- Performance metrics

## Perfect for
- E-commerce businesses
- Service providers
- SaaS companies
- Any business needing customer support
        """,
        "tags": ["customer-service", "automation", "email", "phone", "support"]
    },
    {
        "name": "influencer_agent",
        "seed": "influencer-agent-seed-phrase-12345",
        "port": 8007,
        "url": "http://localhost:8007",
        "title": "Influencer Agent",
        "description": "Finds micro-influencers and drafts outreach campaigns",
        "readme": """
# Influencer Agent

This agent finds and manages influencer marketing campaigns.

## Features
- **Influencer Discovery**: Finds relevant micro-influencers
- **Outreach Templates**: Personalized outreach messages
- **Campaign Strategy**: Comprehensive campaign planning
- **Budget Allocation**: Smart budget distribution
- **Content Briefs**: Detailed content guidelines
- **Performance Tracking**: Campaign metrics and ROI

## Usage
Send an influencer request with:
- Business name and industry
- Target audience
- Budget range
- Campaign goals
- Content types
- Platforms

## Output
- Influencer recommendations
- Outreach templates
- Campaign strategy
- Budget allocation
- Content briefs

## Perfect for
- E-commerce brands
- SaaS companies
- Consumer products
- Lifestyle brands
        """,
        "tags": ["influencer", "marketing", "outreach", "social-media", "campaigns"]
    },
    {
        "name": "pitch_deck_agent",
        "seed": "pitch-deck-agent-seed-phrase-12345",
        "port": 8008,
        "url": "http://localhost:8008",
        "title": "Pitch Deck Agent",
        "description": "Builds investor-ready pitch decks and financial models",
        "readme": """
# Pitch Deck Agent

This agent creates professional pitch decks and financial models for investors.

## Features
- **Pitch Deck Creation**: 10-slide investor presentations
- **Financial Models**: Comprehensive financial projections
- **Investor Notes**: Detailed investor insights
- **Presentation Scripts**: Speaking notes and guidance
- **Market Analysis**: Industry and competitive analysis
- **Team Profiles**: Founder and team information

## Usage
Send a pitch deck request with:
- Business name and idea
- Industry and problem statement
- Solution and target market
- Business model
- Funding amount needed
- Team information

## Output
- Complete pitch deck PDF
- Financial model spreadsheet
- Investor notes
- Presentation script
- Next steps

## Perfect for
- Startups seeking funding
- Entrepreneurs pitching investors
- Accelerator applications
- Demo day presentations
        """,
        "tags": ["pitch-deck", "investors", "funding", "startup", "presentation"]
    }
]

async def deploy_agent(agent_config: Dict[str, Any], api_key: str) -> bool:
    """Deploy a single agent to AgentVerse"""
    try:
        print(f"🚀 Deploying {agent_config['name']}...")
        
        # Create identity from seed
        identity = Identity.from_seed(agent_config["seed"], 0)
        
        # Register with AgentVerse
        result = register_with_agentverse(
            identity=identity,
            url=agent_config["url"],
            agentverse_token=api_key,
            agent_title=agent_config["title"],
            readme=agent_config["readme"]
        )
        
        # Check if registration was successful
        if not result:
            raise Exception("Failed to register with AgentVerse")
        
        print(f"✅ {agent_config['name']} deployed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to deploy {agent_config['name']}: {e}")
        return False

async def deploy_all_agents():
    """Deploy all agents to AgentVerse"""
    # Get API key from environment
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ Error: AGENTVERSE_API_KEY not found in environment variables")
        print("Please set your AgentVerse API key:")
        print("export AGENTVERSE_API_KEY='your-api-key-here'")
        return
    
    print("🎯 Starting deployment of all agents to AgentVerse...")
    print(f"📡 Using API key: {api_key[:10]}...")
    print()
    
    # Deploy each agent
    successful_deployments = 0
    failed_deployments = 0
    
    for agent_config in AGENTS:
        success = await deploy_agent(agent_config, api_key)
        if success:
            successful_deployments += 1
        else:
            failed_deployments += 1
        print()  # Add spacing between deployments
    
    # Summary
    print("=" * 50)
    print("📊 DEPLOYMENT SUMMARY")
    print("=" * 50)
    print(f"✅ Successful deployments: {successful_deployments}")
    print(f"❌ Failed deployments: {failed_deployments}")
    print(f"📈 Success rate: {(successful_deployments / len(AGENTS)) * 100:.1f}%")
    
    if successful_deployments > 0:
        print("\n🎉 Your agents are now live on AgentVerse!")
        print("🔗 Visit https://agentverse.ai to see your agents")
    
    if failed_deployments > 0:
        print(f"\n⚠️  {failed_deployments} agents failed to deploy. Check the errors above.")

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if fetchai is installed
    try:
        import fetchai
        print("✅ fetchai package installed")
    except ImportError:
        print("❌ fetchai package not installed")
        print("Run: pip install fetchai")
        return False
    
    # Check if API key is set
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ AGENTVERSE_API_KEY not set")
        print("Set it with: export AGENTVERSE_API_KEY='your-key'")
        return False
    else:
        print("✅ AGENTVERSE_API_KEY is set")
    
    return True

async def main():
    """Main deployment function"""
    print("🤖 Fetch.ai AgentVerse Deployment Script")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements not met. Please fix the issues above.")
        return
    
    print("\n🚀 Starting deployment...")
    await deploy_all_agents()

if __name__ == "__main__":
    asyncio.run(main())
