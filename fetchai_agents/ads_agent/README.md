# Ads Agent

An AI-powered advertising agent that creates and launches Google and Meta ad campaigns using Veo-3 for video ad generation and CrewAI for orchestration. This agent automates the entire ad creation and deployment process.

## 🎯 Overview

The Ads Agent leverages Google's Veo-3 model for video ad generation and coordinates with Google Ads and Meta Ads APIs to create and launch comprehensive advertising campaigns. It uses CrewAI to manage multiple specialized agents for different aspects of ad creation.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  CrewAI          │───▶│  Veo-3 Video    │
│   (Product,     │    │  Orchestrator    │    │  Generation     │
│   Budget, etc.) │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Google & Meta   │
                       │  Ad Campaigns    │
                       │  Live & Running  │
                       └──────────────────┘
```

## 🚀 Features

### Core Capabilities
- **Video Ad Generation** - AI-powered video ads using Veo-3
- **Campaign Creation** - Google Ads and Meta Ads campaign setup
- **Audience Targeting** - Intelligent audience segmentation
- **Budget Optimization** - Automated budget allocation and bidding
- **A/B Testing** - Multiple ad variations for optimization
- **Performance Monitoring** - Real-time campaign performance tracking
- **Creative Assets** - Images, videos, and copy generation

### Technical Features
- **CrewAI Orchestration** - Multi-agent coordination for ad creation
- **Veo-3 Integration** - Advanced video generation capabilities
- **Multi-Platform Support** - Google Ads and Meta Ads integration
- **Automated Deployment** - Live campaign launch and management

## 🛠️ Technical Implementation

### Dependencies
```python
# Core dependencies
crewai>=0.28.0
google-ads>=22.0.0
facebook-business>=18.0.0
uagents>=0.4.0
fetchai>=0.1.0
pydantic>=2.0.0
requests>=2.31.0
```

### CrewAI Agent Configuration
```python
from crewai import Agent, Task, Crew, Process
from google.ads.googleads.client import GoogleAdsClient
from facebook_business import FacebookAdsApi

# Video Creation Agent
video_agent = Agent(
    role='Video Ad Creator',
    goal='Generate compelling video ads using Veo-3',
    backstory='Expert in video marketing with 6+ years creating viral ad content',
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4o", temperature=0.3)
)

# Campaign Strategy Agent
strategy_agent = Agent(
    role='Ad Campaign Strategist',
    goal='Develop effective ad campaign strategies',
    backstory='Specialist in digital advertising strategy and campaign optimization',
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4o", temperature=0.1)
)

# Platform Deployment Agent
deployment_agent = Agent(
    role='Ad Platform Specialist',
    goal='Deploy campaigns across Google and Meta platforms',
    backstory='Expert in Google Ads and Meta Ads platform management',
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4o", temperature=0.1)
)
```

### Veo-3 Video Generation Integration
```python
import google.generativeai as genai

class VideoAdService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('veo-3')
    
    async def generate_video_ad(self, product_info: dict, campaign_goals: list) -> dict:
        """Generate video ad using Veo-3"""
        
        prompt = f"""
        Create a 15-30 second video advertisement for:
        Product: {product_info['name']}
        Description: {product_info['description']}
        Target Audience: {product_info['target_audience']}
        Campaign Goals: {', '.join(campaign_goals)}
        
        Requirements:
        - Professional quality video
        - Clear call-to-action
        - Engaging visual elements
        - Brand-appropriate tone
        - Mobile-optimized format
        
        Generate video with:
        1. Hook (first 3 seconds)
        2. Problem/solution presentation
        3. Product demonstration
        4. Social proof/testimonial
        5. Clear call-to-action
        """
        
        response = self.model.generate_content(prompt)
        return self.parse_video_response(response.text)
    
    async def generate_ad_variations(self, base_video: dict, count: int = 3) -> list:
        """Generate multiple ad variations for A/B testing"""
        
        variations = []
        for i in range(count):
            variation_prompt = f"""
            Create variation {i+1} of this video ad:
            Base Video: {base_video['description']}
            
            Variation focus:
            - Different hook approach
            - Alternative call-to-action
            - Different visual style
            - Varying length (15-30 seconds)
            """
            
            response = self.model.generate_content(variation_prompt)
            variations.append(self.parse_video_response(response.text))
        
        return variations
```

### Google Ads Integration
```python
from google.ads.googleads.client import GoogleAdsClient

class GoogleAdsService:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        self.client = GoogleAdsClient.load_from_dict({
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "developer_token": "your_developer_token"
        })
    
    async def create_campaign(self, campaign_data: dict) -> dict:
        """Create Google Ads campaign"""
        
        campaign_operation = {
            "create": {
                "name": campaign_data["name"],
                "advertising_channel_type": "VIDEO",
                "status": "PAUSED",
                "budget": {
                    "amount_micros": campaign_data["budget"] * 1000000,
                    "delivery_method": "STANDARD"
                },
                "video_network_settings": {
                    "target_google_video": True,
                    "target_youtube_videos": True,
                    "target_youtube_channels": True
                }
            }
        }
        
        response = self.client.service.campaign_service.mutate_campaigns(
            customer_id=campaign_data["customer_id"],
            operations=[campaign_operation]
        )
        
        return {
            "campaign_id": response.results[0].resource_name,
            "status": "created"
        }
    
    async def create_video_ad(self, ad_data: dict) -> dict:
        """Create video ad in Google Ads"""
        
        ad_operation = {
            "create": {
                "name": ad_data["name"],
                "final_urls": [ad_data["landing_page"]],
                "video": {
                    "asset": ad_data["video_asset_id"]
                }
            }
        }
        
        response = self.client.service.ad_group_ad_service.mutate_ad_group_ads(
            customer_id=ad_data["customer_id"],
            operations=[ad_operation]
        )
        
        return {
            "ad_id": response.results[0].resource_name,
            "status": "created"
        }
```

### Meta Ads Integration
```python
from facebook_business import FacebookAdsApi, AdAccount, Campaign, AdSet, Ad

class MetaAdsService:
    def __init__(self, app_id: str, app_secret: str, access_token: str):
        FacebookAdsApi.init(app_id, app_secret, access_token)
        self.api = FacebookAdsApi.get_default_api()
    
    async def create_campaign(self, campaign_data: dict) -> dict:
        """Create Meta Ads campaign"""
        
        campaign = Campaign.create(
            account_id=campaign_data["account_id"],
            name=campaign_data["name"],
            objective=campaign_data["objective"],
            status="PAUSED"
        )
        
        return {
            "campaign_id": campaign["id"],
            "status": "created"
        }
    
    async def create_video_ad(self, ad_data: dict) -> dict:
        """Create video ad in Meta Ads"""
        
        ad = Ad.create(
            account_id=ad_data["account_id"],
            name=ad_data["name"],
            adset_id=ad_data["adset_id"],
            creative={
                "name": ad_data["creative_name"],
                "object_story_spec": {
                    "video_data": {
                        "video_id": ad_data["video_id"],
                        "message": ad_data["message"],
                        "call_to_action": {
                            "type": ad_data["cta_type"],
                            "value": {"link": ad_data["landing_page"]}
                        }
                    }
                }
            },
            status="PAUSED"
        )
        
        return {
            "ad_id": ad["id"],
            "status": "created"
        }
```

## 📊 API Endpoints

### Main Ad Creation Endpoint
```http
POST /submit
Content-Type: application/json

{
    "product_name": "Smart Fitness Tracker",
    "product_description": "Advanced fitness tracking with AI insights",
    "target_audience": "fitness enthusiasts, 25-45 years old",
    "budget": 1000,
    "campaign_duration": 30,
    "platforms": ["google", "meta"],
    "campaign_goals": ["awareness", "conversions"],
    "creative_style": "modern",
    "call_to_action": "Shop Now"
}
```

### Response Format
```json
{
    "success": true,
    "campaigns": {
        "google_ads": {
            "campaign_id": "campaign_123456",
            "status": "active",
            "budget": 500,
            "ads_created": 3
        },
        "meta_ads": {
            "campaign_id": "campaign_789012",
            "status": "active",
            "budget": 500,
            "ads_created": 3
        }
    },
    "creative_assets": {
        "videos": [
            {
                "id": "video_001",
                "platform": "google",
                "duration": "30s",
                "format": "MP4"
            },
            {
                "id": "video_002",
                "platform": "meta",
                "duration": "15s",
                "format": "MP4"
            }
        ],
        "images": [
            {
                "id": "image_001",
                "platform": "google",
                "format": "JPG",
                "size": "1920x1080"
            }
        ]
    },
    "targeting": {
        "demographics": {
            "age_range": "25-45",
            "gender": "all",
            "interests": ["fitness", "technology", "health"]
        },
        "geographic": {
            "countries": ["US", "CA", "UK"],
            "cities": ["New York", "Los Angeles", "Toronto"]
        }
    }
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_ADS_CLIENT_ID=your_google_ads_client_id
GOOGLE_ADS_CLIENT_SECRET=your_google_ads_client_secret
META_APP_ID=your_meta_app_id
META_APP_SECRET=your_meta_app_secret
META_ACCESS_TOKEN=your_meta_access_token
AGENTVERSE_API_KEY=your_agentverse_api_key_here

# Optional
VEO_MODEL=veo-3
AD_CREATION_TIMEOUT=600
MAX_VIDEO_DURATION=30
```

### Agent Configuration
```python
# Ads Agent settings
ADS_CONFIG = {
    "veo_model": "veo-3",
    "video_duration": "15-30s",
    "timeout": 600,
    "retry_attempts": 3,
    "auto_optimize": True,
    "ab_testing": True,
    "platforms": ["google", "meta"]
}
```

## 🚀 Usage Examples

### Basic Ad Campaign Creation
```python
from ads_agent import AdsAgent

# Initialize agent
agent = AdsAgent()

# Create ad campaign
result = await agent.create_campaign(
    product_name="Eco-Friendly Water Bottle",
    product_description="Sustainable stainless steel water bottle",
    target_audience="eco-conscious consumers, 20-40 years old",
    budget=500,
    platforms=["google", "meta"],
    campaign_goals=["awareness", "conversions"]
)

print(f"Google Campaign: {result['campaigns']['google_ads']}")
print(f"Meta Campaign: {result['campaigns']['meta_ads']}")
```

### Advanced Campaign with Custom Creative
```python
# Advanced campaign creation
result = await agent.create_campaign(
    product_name="AI-Powered Headphones",
    product_description="Noise-canceling headphones with AI sound optimization",
    target_audience="tech enthusiasts, music lovers, 25-50 years old",
    budget=2000,
    platforms=["google", "meta"],
    campaign_goals=["conversions", "brand_awareness"],
    creative_style="tech-forward",
    call_to_action="Pre-order Now",
    video_style="product_demo",
    custom_assets=["logo.png", "product_photos.jpg"]
)
```

## 🔍 Ad Creation Capabilities

### Video Generation
- **Veo-3 Integration** - High-quality video generation
- **Multiple Formats** - Various video lengths and formats
- **A/B Testing** - Multiple video variations
- **Platform Optimization** - Videos optimized for each platform
- **Brand Consistency** - Brand-aligned creative content

### Campaign Management
- **Multi-Platform** - Google Ads and Meta Ads support
- **Budget Optimization** - Intelligent budget allocation
- **Audience Targeting** - Advanced demographic and interest targeting
- **Performance Tracking** - Real-time campaign monitoring
- **Automated Optimization** - AI-powered campaign improvements

### Creative Assets
- **Video Ads** - AI-generated promotional videos
- **Image Ads** - Static image advertisements
- **Copy Generation** - Compelling ad copy and headlines
- **Call-to-Actions** - Effective CTA buttons and text
- **Landing Pages** - Basic landing page optimization

## 🛡️ Security & Privacy

### Data Protection
- **API Key Security** - Encrypted storage and transmission
- **Campaign Data Privacy** - Secure handling of ad data
- **Rate Limiting** - Prevents API abuse
- **Audit Logging** - Complete campaign creation tracking

### Compliance
- **Platform Terms** - Google Ads and Meta Ads compliance
- **Data Privacy** - User data protection
- **Ad Standards** - Platform advertising standards compliance

## 🚀 Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY="your-key"
export GOOGLE_ADS_CLIENT_ID="your-client-id"
export META_APP_ID="your-app-id"
export AGENTVERSE_API_KEY="your-key"

# Run agent
python agent.py
```

### Docker Deployment
```bash
# Build image
docker build -t ads-agent .

# Run container
docker run -p 8004:8004 \
  -e GOOGLE_API_KEY="your-key" \
  -e META_APP_ID="your-app-id" \
  -e AGENTVERSE_API_KEY="your-key" \
  ads-agent
```

### AgentVerse Deployment
```bash
# Deploy to AgentVerse
python deployment/deploy_agents.py
```

## 📚 API Documentation

### Request Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_name` | string | Yes | Name of the product to advertise |
| `product_description` | string | Yes | Product description |
| `target_audience` | string | Yes | Target audience description |
| `budget` | number | Yes | Total campaign budget |
| `platforms` | array | Yes | Advertising platforms to use |
| `campaign_goals` | array | Yes | Campaign objectives |
| `creative_style` | string | No | Creative style preference |
| `call_to_action` | string | No | Call-to-action text |

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Request success status |
| `campaigns` | object | Created campaigns by platform |
| `creative_assets` | object | Generated creative assets |
| `targeting` | object | Audience targeting configuration |
| `performance_metrics` | object | Initial performance data |

## 🔧 Troubleshooting

### Common Issues
1. **API Rate Limits** - Implement retry logic with exponential backoff
2. **Video Generation Errors** - Check Veo-3 API availability
3. **Campaign Creation Failures** - Validate ad account permissions
4. **Creative Approval** - Ensure content meets platform guidelines

### Debug Mode
```bash
# Enable debug logging
export AGENT_DEBUG=true
export LOG_LEVEL=DEBUG

# Run with verbose output
python agent.py --verbose
```

## 📞 Support

- **Documentation**: [AgentVerse Docs](https://docs.agentverse.ai)
- **Google Ads API**: [Google Ads Developer Docs](https://developers.google.com/google-ads)
- **Meta Ads API**: [Meta for Developers](https://developers.facebook.com)
- **Issues**: Create GitHub issues for bugs
- **Community**: Join Fetch.ai Discord

---

**Built with ❤️ using CrewAI orchestration and Veo-3 video generation**
