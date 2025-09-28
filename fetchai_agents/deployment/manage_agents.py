"""
Agent management script for AgentVerse quota management
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import requests
import json

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from fetchai.registration import register_with_agentverse
    from uagents_core.identity import Identity
except ImportError:
    print("Error: fetchai package not installed. Run: pip install fetchai")
    sys.exit(1)

# Priority agents (most important ones to deploy first)
PRIORITY_AGENTS = [
    "market_research_agent",
    "branding_agent", 
    "shopify_agent",
    "ads_agent"
]

# Secondary agents (deploy after priority ones)
SECONDARY_AGENTS = [
    "legal_docs_agent",
    "customer_service_agent",
    "influencer_agent",
    "pitch_deck_agent"
]

# Agent configurations (same as deploy_agents.py)
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

def get_agent_config(name: str) -> Dict[str, Any]:
    """Get agent configuration by name"""
    for agent in AGENTS:
        if agent["name"] == name:
            return agent
    raise ValueError(f"Agent {name} not found")

async def deploy_priority_agents():
    """Deploy only the priority agents (within quota limit)"""
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ Error: AGENTVERSE_API_KEY not found in environment variables")
        return
    
    print("🎯 Deploying Priority Agents (within quota limit)...")
    print("=" * 50)
    
    successful_deployments = 0
    failed_deployments = 0
    
    for agent_name in PRIORITY_AGENTS:
        try:
            agent_config = get_agent_config(agent_name)
            print(f"🚀 Deploying {agent_name}...")
            
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
            
            if result:
                print(f"✅ {agent_name} deployed successfully!")
                successful_deployments += 1
            else:
                print(f"❌ {agent_name} deployment failed")
                failed_deployments += 1
                
        except Exception as e:
            print(f"❌ Failed to deploy {agent_name}: {e}")
            failed_deployments += 1
        
        print()  # Add spacing
    
    # Summary
    print("=" * 50)
    print("📊 PRIORITY AGENTS DEPLOYMENT SUMMARY")
    print("=" * 50)
    print(f"✅ Successful deployments: {successful_deployments}")
    print(f"❌ Failed deployments: {failed_deployments}")
    print(f"📈 Success rate: {(successful_deployments / len(PRIORITY_AGENTS)) * 100:.1f}%")

async def deploy_secondary_agents():
    """Deploy secondary agents (may hit quota limit)"""
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ Error: AGENTVERSE_API_KEY not found in environment variables")
        return
    
    print("🎯 Deploying Secondary Agents...")
    print("⚠️  Note: This may hit your quota limit")
    print("=" * 50)
    
    successful_deployments = 0
    failed_deployments = 0
    
    for agent_name in SECONDARY_AGENTS:
        try:
            agent_config = get_agent_config(agent_name)
            print(f"🚀 Deploying {agent_name}...")
            
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
            
            if result:
                print(f"✅ {agent_name} deployed successfully!")
                successful_deployments += 1
            else:
                print(f"❌ {agent_name} deployment failed")
                failed_deployments += 1
                
        except Exception as e:
            print(f"❌ Failed to deploy {agent_name}: {e}")
            failed_deployments += 1
        
        print()  # Add spacing
    
    # Summary
    print("=" * 50)
    print("📊 SECONDARY AGENTS DEPLOYMENT SUMMARY")
    print("=" * 50)
    print(f"✅ Successful deployments: {successful_deployments}")
    print(f"❌ Failed deployments: {failed_deployments}")
    print(f"📈 Success rate: {(successful_deployments / len(SECONDARY_AGENTS)) * 100:.1f}%")

def show_quota_info():
    """Show information about AgentVerse quota limits"""
    print("📊 AgentVerse Quota Information")
    print("=" * 40)
    print("🔢 Current quota limit: 4 agents")
    print("📈 Priority agents (recommended): 4")
    print("📋 Secondary agents: 4")
    print()
    print("💡 Recommendation:")
    print("   1. Deploy priority agents first (4 agents)")
    print("   2. Upgrade your plan for more agents")
    print("   3. Or deploy secondary agents one by one")
    print()

def show_agent_list():
    """Show list of all available agents"""
    print("🤖 Available Agents")
    print("=" * 30)
    print()
    
    print("🎯 PRIORITY AGENTS (Deploy first):")
    for i, agent_name in enumerate(PRIORITY_AGENTS, 1):
        agent = get_agent_config(agent_name)
        print(f"   {i}. {agent['title']}")
        print(f"      {agent['description']}")
        print()
    
    print("📋 SECONDARY AGENTS (Deploy after priority):")
    for i, agent_name in enumerate(SECONDARY_AGENTS, 1):
        agent = get_agent_config(agent_name)
        print(f"   {i}. {agent['title']}")
        print(f"      {agent['description']}")
        print()

async def main():
    """Main management function"""
    print("🤖 AgentVerse Agent Management")
    print("=" * 40)
    
    # Check API key
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ Error: AGENTVERSE_API_KEY not found")
        print("Set it with: export AGENTVERSE_API_KEY='your-key'")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    print()
    
    # Show options
    print("Choose an option:")
    print("1. Show agent list")
    print("2. Deploy priority agents (4 agents)")
    print("3. Deploy secondary agents (4 agents)")
    print("4. Deploy all agents (8 agents - may hit quota)")
    print("5. Show quota information")
    print()
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        show_agent_list()
    elif choice == "2":
        await deploy_priority_agents()
    elif choice == "3":
        await deploy_secondary_agents()
    elif choice == "4":
        print("⚠️  Warning: This will likely hit your quota limit!")
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm == 'y':
            await deploy_priority_agents()
            await deploy_secondary_agents()
        else:
            print("Cancelled.")
    elif choice == "5":
        show_quota_info()
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    asyncio.run(main())
