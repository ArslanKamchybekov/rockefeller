# Branding Agent

An AI-powered branding agent that generates comprehensive brand identities using Google Gemini for creative content generation and CrewAI for orchestration. This agent creates logos, taglines, color schemes, and complete brand guidelines for businesses.

## 🎯 Overview

The Branding Agent leverages Google Gemini's creative capabilities to generate brand names, taglines, color palettes, and visual concepts. It uses CrewAI to coordinate multiple specialized agents for different aspects of brand creation.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  CrewAI          │───▶│  Google Gemini  │
│   (Business     │    │  Orchestrator    │    │  Creative AI    │
│   Idea, etc.)   │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Brand Assets    │
                       │  Generation      │
                       │  & Guidelines    │
                       └──────────────────┘
```

## 🚀 Features

### Core Capabilities
- **Brand Name Generation** - Creative and memorable business names
- **Tagline Creation** - Compelling slogans and brand messages
- **Color Scheme Design** - Cohesive color palettes and combinations
- **Logo Concepts** - Detailed logo descriptions and visual concepts
- **Brand Guidelines** - Complete brand style guides and usage rules
- **Visual Assets** - Business cards, social media templates, and marketing materials

### Technical Features
- **CrewAI Orchestration** - Multi-agent coordination for brand creation
- **Google Gemini Integration** - Advanced creative AI capabilities
- **Structured Output** - Well-formatted brand assets and guidelines
- **Customization** - Industry-specific and audience-targeted branding

## 🛠️ Technical Implementation

### Dependencies
```python
# Core dependencies
crewai>=0.28.0
google-generativeai>=0.3.0
uagents>=0.4.0
fetchai>=0.1.0
pydantic>=2.0.0
requests>=2.31.0
```

### CrewAI Agent Configuration
```python
from crewai import Agent, Task, Crew, Process
import google.generativeai as genai

# Brand Name Agent
brand_name_agent = Agent(
    role='Creative Brand Naming Specialist',
    goal='Generate memorable and relevant brand names',
    backstory='Expert in brand naming with 8+ years creating names for startups and enterprises',
    verbose=True,
    allow_delegation=False,
    llm=genai.GenerativeModel('gemini-pro')
)

# Tagline Agent
tagline_agent = Agent(
    role='Brand Messaging Specialist',
    goal='Create compelling taglines and brand messages',
    backstory='Specialist in brand messaging and copywriting for various industries',
    verbose=True,
    allow_delegation=False,
    llm=genai.GenerativeModel('gemini-pro')
)

# Visual Design Agent
visual_agent = Agent(
    role='Visual Brand Designer',
    goal='Design color schemes and visual brand elements',
    backstory='Expert in visual design and brand identity creation',
    verbose=True,
    allow_delegation=False,
    llm=genai.GenerativeModel('gemini-pro')
)
```

### Google Gemini Integration
```python
import google.generativeai as genai

class BrandingService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_brand_name(self, business_idea: str, industry: str) -> str:
        """Generate brand names using Gemini"""
        
        prompt = f"""
        Generate 5 creative brand names for a {industry} business with this concept: {business_idea}
        
        Requirements:
        - Memorable and easy to pronounce
        - Relevant to the industry
        - Available domain potential
        - Professional yet creative
        - 2-3 words maximum
        
        Format as a JSON array of names with brief explanations.
        """
        
        response = self.model.generate_content(prompt)
        return self.parse_brand_names(response.text)
    
    async def generate_tagline(self, brand_name: str, business_idea: str) -> str:
        """Generate taglines using Gemini"""
        
        prompt = f"""
        Create 3 compelling taglines for "{brand_name}" - a {business_idea} business.
        
        Requirements:
        - 3-8 words maximum
        - Clear value proposition
        - Memorable and catchy
        - Industry-appropriate tone
        - Action-oriented
        
        Format as a JSON array with taglines and explanations.
        """
        
        response = self.model.generate_content(prompt)
        return self.parse_taglines(response.text)
    
    async def generate_color_scheme(self, industry: str, brand_personality: list) -> dict:
        """Generate color schemes using Gemini"""
        
        prompt = f"""
        Design a professional color palette for a {industry} brand with personality: {', '.join(brand_personality)}
        
        Provide:
        - Primary color (hex code)
        - Secondary color (hex code)
        - Accent color (hex code)
        - Neutral color (hex code)
        - Color psychology explanation
        - Usage guidelines
        
        Format as JSON with color codes and descriptions.
        """
        
        response = self.model.generate_content(prompt)
        return self.parse_color_scheme(response.text)
```

## 📊 API Endpoints

### Main Branding Endpoint
```http
POST /submit
Content-Type: application/json

{
    "business_idea": "AI-powered fitness app",
    "industry": "healthcare",
    "target_audience": "fitness enthusiasts",
    "brand_personality": ["modern", "energetic", "professional"],
    "color_preferences": ["blue", "green"],
    "style_preferences": ["minimalist", "tech-focused"]
}
```

### Response Format
```json
{
    "success": true,
    "brand_name": "FitAI Pro",
    "tagline": "Transform Your Fitness with AI",
    "color_scheme": {
        "primary": "#2563eb",
        "secondary": "#10b981",
        "accent": "#f59e0b",
        "neutral": "#f8fafc"
    },
    "logo_description": "Modern logo with AI circuit pattern and fitness icon",
    "brand_guidelines": {
        "logo_usage": {
            "minimum_size": "100px",
            "clear_space": "50px",
            "backgrounds": ["white", "black", "primary_color"]
        },
        "typography": {
            "primary_font": "Inter",
            "secondary_font": "Open Sans"
        },
        "voice_tone": {
            "personality": ["modern", "energetic"],
            "tone": "motivational",
            "style": "conversational"
        }
    },
    "visual_assets": [
        {
            "type": "logo",
            "description": "Primary logo with AI and fitness elements",
            "formats": ["PNG", "SVG", "PDF"]
        },
        {
            "type": "business_cards",
            "description": "Professional business cards with brand colors"
        }
    ]
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
GOOGLE_API_KEY=your_google_api_key_here
AGENTVERSE_API_KEY=your_agentverse_api_key_here

# Optional
GEMINI_MODEL=gemini-pro
BRANDING_TIMEOUT=60
MAX_ITERATIONS=3
```

### Agent Configuration
```python
# Branding Agent settings
BRANDING_CONFIG = {
    "model": "gemini-pro",
    "temperature": 0.7,
    "max_tokens": 2000,
    "timeout": 60,
    "retry_attempts": 2,
    "creative_mode": True,
    "industry_specific": True
}
```

## 🚀 Usage Examples

### Basic Brand Generation
```python
from branding_agent import BrandingAgent

# Initialize agent
agent = BrandingAgent()

# Generate brand identity
result = await agent.generate_branding(
    business_idea="sustainable fashion marketplace",
    industry="fashion",
    target_audience="eco-conscious consumers",
    brand_personality=["sustainable", "modern", "ethical"]
)

print(f"Brand Name: {result['brand_name']}")
print(f"Tagline: {result['tagline']}")
print(f"Colors: {result['color_scheme']}")
```

### Advanced Branding with Custom Requirements
```python
# Advanced branding with specific requirements
result = await agent.generate_branding(
    business_idea="AI-powered legal document automation",
    industry="legal",
    target_audience="law firms and legal professionals",
    brand_personality=["professional", "innovative", "trustworthy"],
    color_preferences=["navy", "gold"],
    style_preferences=["corporate", "tech-forward"]
)
```

## 🔍 Brand Generation Capabilities

### Brand Naming
- **Creative Generation** - AI-powered name creation
- **Industry Relevance** - Names appropriate for specific industries
- **Memorability** - Easy to remember and pronounce
- **Domain Availability** - Consideration for web presence
- **Trademark Awareness** - Basic trademark considerations

### Visual Identity
- **Color Psychology** - Colors that match brand personality
- **Typography Selection** - Fonts that convey brand values
- **Logo Concepts** - Detailed logo descriptions and concepts
- **Style Guidelines** - Usage rules and best practices

### Brand Guidelines
- **Logo Usage** - Size, spacing, and background requirements
- **Color Applications** - Primary, secondary, and accent usage
- **Typography Rules** - Font hierarchy and text styling
- **Voice and Tone** - Brand personality and communication style

## 🛡️ Security & Privacy

### Data Protection
- **API Key Security** - Encrypted storage and transmission
- **Input Sanitization** - Secure handling of user inputs
- **Rate Limiting** - Prevents API abuse
- **Audit Logging** - Request tracking and monitoring

### Compliance
- **Data Privacy** - User data protection
- **API Terms** - Google Gemini usage compliance
- **Content Guidelines** - Appropriate content generation

## 🚀 Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY="your-key"
export AGENTVERSE_API_KEY="your-key"

# Run agent
python agent.py
```

### Docker Deployment
```bash
# Build image
docker build -t branding-agent .

# Run container
docker run -p 8002:8002 \
  -e GOOGLE_API_KEY="your-key" \
  -e AGENTVERSE_API_KEY="your-key" \
  branding-agent
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
| `business_idea` | string | Yes | Business concept or idea |
| `industry` | string | Yes | Industry category |
| `target_audience` | string | Yes | Target customer segment |
| `brand_personality` | array | No | Brand personality traits |
| `color_preferences` | array | No | Preferred colors |
| `style_preferences` | array | No | Design style preferences |

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Request success status |
| `brand_name` | string | Generated brand name |
| `tagline` | string | Brand tagline/slogan |
| `color_scheme` | object | Color palette with hex codes |
| `logo_description` | string | Logo concept description |
| `brand_guidelines` | object | Brand usage guidelines |
| `visual_assets` | array | Generated visual assets |

## 🔧 Troubleshooting

### Common Issues
1. **API Rate Limits** - Implement retry logic with backoff
2. **Content Filtering** - Adjust prompts for appropriate content
3. **Model Responses** - Handle parsing errors gracefully
4. **Timeout Issues** - Increase timeout settings

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
- **Issues**: Create GitHub issues for bugs
- **Community**: Join Fetch.ai Discord
- **Email**: support@agentverse.ai

---

**Built with ❤️ using CrewAI orchestration and Google Gemini creative AI**
