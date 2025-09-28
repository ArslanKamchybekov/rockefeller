"""
Test script for all Fetch.ai agents
"""

import asyncio
import requests
import json
import time
from typing import List, Dict, Any

# Test configurations for each agent
AGENT_TESTS = [
    {
        "name": "market_research_agent",
        "port": 8001,
        "url": "http://localhost:8001",
        "test_data": {
            "industry": "technology",
            "region": "global",
            "focus_areas": ["trends", "competitors", "demand"],
            "budget_range": "1000-5000"
        }
    },
    {
        "name": "branding_agent",
        "port": 8002,
        "url": "http://localhost:8002",
        "test_data": {
            "business_idea": "AI-powered fitness app",
            "industry": "healthcare",
            "target_audience": "fitness enthusiasts",
            "brand_personality": ["modern", "energetic"]
        }
    },
    {
        "name": "shopify_agent",
        "port": 8003,
        "url": "http://localhost:8003",
        "test_data": {
            "store_name": "Test Fitness Store",
            "industry": "fitness",
            "products": [
                {"name": "Fitness Tracker", "price": "99.99", "description": "Smart fitness tracker"}
            ],
            "theme_preference": "modern"
        }
    },
    {
        "name": "ads_agent",
        "port": 8004,
        "url": "http://localhost:8004",
        "test_data": {
            "business_name": "Test Fitness App",
            "industry": "healthcare",
            "target_audience": {"age_range": "25-45", "interests": ["fitness", "health"]},
            "budget": 1000,
            "duration_days": 30,
            "platforms": ["google", "meta"]
        }
    },
    {
        "name": "legal_docs_agent",
        "port": 8005,
        "url": "http://localhost:8005",
        "test_data": {
            "business_name": "Test Fitness LLC",
            "business_type": "LLC",
            "industry": "healthcare",
            "state": "Delaware",
            "business_address": {"address": "123 Test St", "city": "Test City", "state": "DE", "zip": "12345"},
            "owner_info": {"name": "John Doe", "email": "john@test.com"},
            "required_documents": ["privacy_policy", "terms_of_service"]
        }
    },
    {
        "name": "customer_service_agent",
        "port": 8006,
        "url": "http://localhost:8006",
        "test_data": {
            "business_name": "Test Fitness App",
            "industry": "healthcare",
            "service_types": ["email_templates", "phone_automation"],
            "phone_number": "+1234567890",
            "business_hours": {"start": "9:00 AM", "end": "5:00 PM", "timezone": "EST"}
        }
    },
    {
        "name": "influencer_agent",
        "port": 8007,
        "url": "http://localhost:8007",
        "test_data": {
            "business_name": "Test Fitness App",
            "industry": "healthcare",
            "target_audience": {"age_range": "25-45", "interests": ["fitness", "wellness"]},
            "budget_range": "1000-5000",
            "campaign_goals": ["brand_awareness", "engagement"],
            "platforms": ["instagram", "tiktok"]
        }
    },
    {
        "name": "pitch_deck_agent",
        "port": 8008,
        "url": "http://localhost:8008",
        "test_data": {
            "business_name": "Test Fitness App",
            "industry": "healthcare",
            "business_idea": "AI-powered fitness app",
            "problem_statement": "People struggle to maintain consistent fitness routines",
            "solution": "AI-powered personal trainer app",
            "target_market": "Fitness enthusiasts aged 25-45",
            "business_model": "Subscription-based SaaS",
            "funding_amount": 500000,
            "team_info": [{"name": "John Doe", "role": "CEO", "background": "Former fitness trainer"}]
        }
    }
]

async def test_agent(agent_config: Dict[str, Any]) -> Dict[str, Any]:
    """Test a single agent"""
    agent_name = agent_config["name"]
    port = agent_config["port"]
    url = agent_config["url"]
    test_data = agent_config["test_data"]
    
    print(f"🧪 Testing {agent_name} on port {port}...")
    
    try:
        # Test health endpoint
        health_response = requests.get(f"{url}/health", timeout=5)
        health_status = health_response.status_code == 200
        
        # Test main agent endpoint
        main_response = requests.post(
            f"{url}/submit",
            json=test_data,
            timeout=30
        )
        main_status = main_response.status_code == 200
        
        if main_status:
            response_data = main_response.json()
            success = response_data.get("success", False)
        else:
            success = False
            response_data = {"error": f"HTTP {main_response.status_code}"}
        
        return {
            "agent_name": agent_name,
            "port": port,
            "health_check": health_status,
            "main_endpoint": main_status,
            "success": success,
            "response_data": response_data,
            "error": None
        }
        
    except requests.exceptions.ConnectionError:
        return {
            "agent_name": agent_name,
            "port": port,
            "health_check": False,
            "main_endpoint": False,
            "success": False,
            "response_data": None,
            "error": "Connection refused - agent not running"
        }
    except requests.exceptions.Timeout:
        return {
            "agent_name": agent_name,
            "port": port,
            "health_check": False,
            "main_endpoint": False,
            "success": False,
            "response_data": None,
            "error": "Request timeout"
        }
    except Exception as e:
        return {
            "agent_name": agent_name,
            "port": port,
            "health_check": False,
            "main_endpoint": False,
            "success": False,
            "response_data": None,
            "error": str(e)
        }

async def test_all_agents():
    """Test all agents"""
    print("🧪 Testing all Fetch.ai agents...")
    print("=" * 50)
    
    results = []
    
    for agent_config in AGENT_TESTS:
        result = await test_agent(agent_config)
        results.append(result)
        
        # Print individual result
        if result["success"]:
            print(f"✅ {result['agent_name']} - PASSED")
        else:
            print(f"❌ {result['agent_name']} - FAILED")
            if result["error"]:
                print(f"   Error: {result['error']}")
        
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for r in results if r["success"])
    failed = len(results) - passed
    
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success rate: {(passed / len(results)) * 100:.1f}%")
    
    # Detailed results
    print("\n📋 DETAILED RESULTS:")
    print("-" * 30)
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        health = "🟢" if result["health_check"] else "🔴"
        main = "🟢" if result["main_endpoint"] else "🔴"
        
        print(f"{result['agent_name']:<25} {status} Health: {health} Main: {main}")
        
        if result["error"]:
            print(f"  └─ Error: {result['error']}")
    
    return results

def check_agent_ports():
    """Check if any agents are running on expected ports"""
    print("🔍 Checking for running agents...")
    
    running_agents = []
    for agent_config in AGENT_TESTS:
        try:
            response = requests.get(f"http://localhost:{agent_config['port']}/health", timeout=2)
            if response.status_code == 200:
                running_agents.append(agent_config["name"])
        except:
            pass
    
    if running_agents:
        print(f"✅ Found {len(running_agents)} running agents: {', '.join(running_agents)}")
    else:
        print("❌ No agents found running. Start them with: python deployment/start_agents.py")
    
    return len(running_agents) > 0

async def main():
    """Main test function"""
    print("🤖 Fetch.ai Agent Testing Suite")
    print("=" * 50)
    
    # Check if agents are running
    if not check_agent_ports():
        print("\n⚠️  Please start the agents first:")
        print("   python deployment/start_agents.py")
        return
    
    print("\n🚀 Starting agent tests...")
    await test_all_agents()

if __name__ == "__main__":
    asyncio.run(main())
