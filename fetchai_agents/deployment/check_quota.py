"""
Script to check AgentVerse quota and existing agents
"""

import os
import requests
import json
from typing import Dict, Any, List

def check_agentverse_quota(api_key: str) -> Dict[str, Any]:
    """Check AgentVerse quota and existing agents"""
    try:
        # This is a placeholder - the actual API endpoint may vary
        # You might need to check the AgentVerse documentation for the correct endpoint
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Try to get agent information
        response = requests.get(
            "https://agentverse.ai/v1/agents",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "agents": data.get("agents", []),
                "quota": data.get("quota", {}),
                "total_agents": len(data.get("agents", []))
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "agents": [],
                "quota": {},
                "total_agents": 0
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agents": [],
            "quota": {},
            "total_agents": 0
        }

def display_quota_info(quota_data: Dict[str, Any]):
    """Display quota information in a readable format"""
    print("📊 AgentVerse Quota Status")
    print("=" * 40)
    
    if not quota_data["success"]:
        print(f"❌ Error checking quota: {quota_data['error']}")
        print()
        print("💡 This might be because:")
        print("   - The API endpoint has changed")
        print("   - Your API key doesn't have the right permissions")
        print("   - There's a network issue")
        return
    
    total_agents = quota_data["total_agents"]
    quota_info = quota_data["quota"]
    
    print(f"🤖 Total agents deployed: {total_agents}")
    
    if quota_info:
        limit = quota_info.get("limit", "Unknown")
        used = quota_info.get("used", total_agents)
        remaining = quota_info.get("remaining", "Unknown")
        
        print(f"📈 Quota limit: {limit}")
        print(f"✅ Used: {used}")
        print(f"🔄 Remaining: {remaining}")
    else:
        print("📈 Quota limit: 4 (default)")
        print(f"✅ Used: {total_agents}")
        remaining = 4 - total_agents
        print(f"🔄 Remaining: {remaining}")
    
    print()
    
    if total_agents > 0:
        print("📋 Deployed Agents:")
        print("-" * 20)
        for i, agent in enumerate(quota_data["agents"], 1):
            name = agent.get("name", "Unknown")
            title = agent.get("title", "No title")
            status = agent.get("status", "Unknown")
            print(f"   {i}. {name} - {title} ({status})")
    else:
        print("📋 No agents deployed yet")
    
    print()
    
    # Recommendations
    if total_agents >= 4:
        print("⚠️  QUOTA FULL!")
        print("💡 Recommendations:")
        print("   1. Upgrade your AgentVerse plan for more agents")
        print("   2. Remove unused agents to free up space")
        print("   3. Use the manage_agents.py script to prioritize agents")
    elif total_agents > 0:
        remaining = 4 - total_agents
        print(f"✅ You can deploy {remaining} more agents")
        print("💡 Use manage_agents.py to deploy priority agents")
    else:
        print("✅ You can deploy up to 4 agents")
        print("💡 Use manage_agents.py to deploy priority agents")

def main():
    """Main function"""
    print("🔍 Checking AgentVerse Quota...")
    print()
    
    # Get API key
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ Error: AGENTVERSE_API_KEY not found")
        print("Set it with: export AGENTVERSE_API_KEY='your-key'")
        return
    
    print(f"🔑 Using API key: {api_key[:10]}...")
    print()
    
    # Check quota
    quota_data = check_agentverse_quota(api_key)
    display_quota_info(quota_data)

if __name__ == "__main__":
    main()
