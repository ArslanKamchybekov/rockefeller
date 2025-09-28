# Fetch.ai AgentVerse Agents

A comprehensive collection of 8 AI agents designed for business automation and deployed on Fetch.ai's AgentVerse platform.

## 🤖 Agents Overview

| Agent | Port | Description |
|-------|------|-------------|
| **Market Research** | 8001 | Finds trending niches and analyzes product demand |
| **Branding** | 8002 | Creates logos, taglines, color schemes, and visual assets |
| **Shopify Store** | 8003 | Creates and publishes Shopify storefronts |
| **Ads** | 8004 | Launches Google and Meta advertising campaigns |
| **Legal Docs** | 8005 | Auto-generates LLC docs, policies, and Terms of Service |
| **Customer Service** | 8006 | Drafts email templates and automates customer responses |
| **Influencer** | 8007 | Finds micro-influencers and drafts outreach campaigns |
| **Pitch Deck** | 8008 | Builds investor-ready pitch decks and financial models |

## 🚀 Quick Start

### Prerequisites

1. **Python 3.11+**
2. **AgentVerse API Key** - Get from [AgentVerse](https://agentverse.ai)
3. **Docker** (optional, for containerized deployment)

### Installation

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd fetchai_agents
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   cp env.example .env
   # Edit .env and add your AGENTVERSE_API_KEY
   export AGENTVERSE_API_KEY="your-api-key-here"
   ```

### Running Agents

#### Option 1: Local Development
```bash
# Start all agents locally
python deployment/start_agents.py

# Deploy to AgentVerse
python deployment/deploy_agents.py
```

#### Option 2: Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Deploy to AgentVerse (run in another terminal)
python deployment/deploy_agents.py
```

## 📋 Agent Details

### 1. Market Research Agent
- **Purpose**: Market analysis and trend identification
- **Input**: Industry, region, focus areas, budget range
- **Output**: Market insights, competitor analysis, trending products
- **Use Cases**: Business validation, market entry, competitive analysis

### 2. Branding Agent
- **Purpose**: Complete brand identity creation
- **Input**: Business idea, industry, target audience, brand personality
- **Output**: Brand name, tagline, color scheme, logo concepts, brand guidelines
- **Use Cases**: Startup branding, rebranding, brand identity

### 3. Shopify Store Agent
- **Purpose**: E-commerce store creation and management
- **Input**: Store name, industry, products, theme preferences
- **Output**: Live store URL, admin access, store configuration
- **Use Cases**: E-commerce launch, dropshipping, online selling

### 4. Ads Agent
- **Purpose**: Multi-platform advertising campaign management
- **Input**: Business details, target audience, budget, platforms
- **Output**: Campaign IDs, ad creatives, targeting setup, performance metrics
- **Use Cases**: Digital marketing, customer acquisition, brand awareness

### 5. Legal Docs Agent
- **Purpose**: Legal document generation and compliance
- **Input**: Business details, document types, state, owner info
- **Output**: Legal documents, filing requirements, compliance checklist
- **Use Cases**: Business formation, legal compliance, document automation

### 6. Customer Service Agent
- **Purpose**: Customer service automation and support
- **Input**: Business details, service types, phone number, business hours
- **Output**: Email templates, phone automation, chat responses, VAPI setup
- **Use Cases**: Customer support, service automation, response management

### 7. Influencer Agent
- **Purpose**: Influencer marketing and outreach
- **Input**: Business details, target audience, budget, campaign goals
- **Output**: Influencer recommendations, outreach templates, campaign strategy
- **Use Cases**: Influencer marketing, brand partnerships, social media campaigns

### 8. Pitch Deck Agent
- **Purpose**: Investor presentation and financial modeling
- **Input**: Business idea, funding amount, team info, financial projections
- **Output**: Pitch deck PDF, financial model, investor notes, presentation script
- **Use Cases**: Fundraising, investor presentations, startup pitches

## 🔧 Configuration

### Environment Variables

```bash
# Required
AGENTVERSE_API_KEY=your_agentverse_api_key_here

# Optional
AGENT_DEBUG=false
AGENT_LOG_LEVEL=INFO
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
SHOPIFY_API_KEY=your_shopify_key
```

### Agent Customization

Each agent can be customized by modifying the respective `agent.py` file in its directory. Key customization points:

- **Business logic**: Modify the core functions
- **API integrations**: Add external service connections
- **Response formats**: Customize output structures
- **Validation**: Add input validation rules

## 📊 Monitoring and Analytics

### Health Checks
- Each agent exposes a `/health` endpoint
- Docker health checks monitor agent status
- Logs are available in the `logs/` directory

### Performance Metrics
- Response times
- Success rates
- Error tracking
- Usage statistics

## 🚀 Deployment to AgentVerse

### **Important: Quota Management**
AgentVerse has a quota limit of **4 agents** on the free tier. Use the management scripts to deploy strategically.

### **Step-by-Step Deployment:**

1. **Check your current quota:**
   ```bash
   python deployment/check_quota.py
   ```

2. **Start agents locally:**
   ```bash
   python deployment/start_agents.py
   ```

3. **Deploy priority agents (recommended):**
   ```bash
   python deployment/manage_agents.py
   # Choose option 2: Deploy priority agents (4 agents)
   ```

4. **Or deploy all agents (may hit quota):**
   ```bash
   python deployment/deploy_agents.py
   ```

5. **Verify deployment:**
   - Visit [AgentVerse](https://agentverse.ai)
   - Search for your agents
   - Test agent functionality

### **Priority Agents (Deploy First):**
1. **Market Research Agent** - Essential for business validation
2. **Branding Agent** - Critical for brand identity
3. **Shopify Store Agent** - Key for e-commerce
4. **Ads Agent** - Important for marketing

### **Secondary Agents (Deploy After):**
5. **Legal Docs Agent** - Important for compliance
6. **Customer Service Agent** - Useful for support
7. **Influencer Agent** - Good for marketing
8. **Pitch Deck Agent** - Helpful for fundraising

## 🔍 Testing Agents

### Individual Agent Testing
```bash
# Test a specific agent
curl -X POST http://localhost:8001/submit \
  -H "Content-Type: application/json" \
  -d '{"industry": "technology", "region": "global"}'
```

### Batch Testing
```bash
# Test all agents
python deployment/test_agents.py
```

## 📚 API Documentation

Each agent exposes a REST API with the following endpoints:

- `POST /submit` - Main agent endpoint
- `GET /health` - Health check
- `GET /status` - Agent status
- `GET /docs` - API documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check individual agent README files
- **Issues**: Create GitHub issues for bugs or feature requests
- **Community**: Join the Fetch.ai community for support

## 🔗 Links

- [Fetch.ai Documentation](https://docs.fetch.ai)
- [AgentVerse Platform](https://agentverse.ai)
- [uAgents Framework](https://github.com/fetchai/uAgents)

---

**Built with ❤️ for the Fetch.ai ecosystem**
