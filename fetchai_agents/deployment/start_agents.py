"""
Script to start all Fetch.ai agents locally
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path
import signal
import os

# Agent configurations
AGENTS = [
    {
        "name": "market_research_agent",
        "script": "market_research_agent/agent.py",
        "port": 8001
    },
    {
        "name": "branding_agent", 
        "script": "branding_agent/agent.py",
        "port": 8002
    },
    {
        "name": "shopify_agent",
        "script": "shopify_agent/agent.py", 
        "port": 8003
    },
    {
        "name": "ads_agent",
        "script": "ads_agent/agent.py",
        "port": 8004
    },
    {
        "name": "legal_docs_agent",
        "script": "legal_docs_agent/agent.py",
        "port": 8005
    },
    {
        "name": "customer_service_agent",
        "script": "customer_service_agent/agent.py",
        "port": 8006
    },
    {
        "name": "influencer_agent",
        "script": "influencer_agent/agent.py",
        "port": 8007
    },
    {
        "name": "pitch_deck_agent",
        "script": "pitch_deck_agent/agent.py",
        "port": 8008
    }
]

# Store process references
processes = []

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Shutting down all agents...")
    for process in processes:
        if process.poll() is None:  # Process is still running
            process.terminate()
    sys.exit(0)

def start_agent(agent_config):
    """Start a single agent"""
    try:
        print(f"🚀 Starting {agent_config['name']} on port {agent_config['port']}...")
        
        # Change to the parent directory
        parent_dir = Path(__file__).parent.parent
        script_path = parent_dir / agent_config["script"]
        
        # Start the agent process
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            cwd=parent_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        processes.append(process)
        print(f"✅ {agent_config['name']} started (PID: {process.pid})")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start {agent_config['name']}: {e}")
        return None

def check_agent_health(agent_config):
    """Check if an agent is responding"""
    try:
        import requests
        response = requests.get(f"http://localhost:{agent_config['port']}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main function to start all agents"""
    print("🤖 Starting all Fetch.ai agents...")
    print("=" * 50)
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check if requirements are installed
    try:
        import uagents
        import fetchai
        print("✅ Required packages are installed")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return
    
    # Start all agents
    started_agents = []
    for agent_config in AGENTS:
        process = start_agent(agent_config)
        if process:
            started_agents.append(agent_config)
        time.sleep(2)  # Give each agent time to start
    
    if not started_agents:
        print("❌ No agents started successfully")
        return
    
    print(f"\n✅ {len(started_agents)} agents started successfully!")
    print("\n📊 Agent Status:")
    print("-" * 30)
    
    for agent_config in started_agents:
        status = "🟢 Running" if check_agent_health(agent_config) else "🟡 Starting..."
        print(f"{agent_config['name']:<25} {status}")
    
    print(f"\n🌐 Agents are running on:")
    for agent_config in started_agents:
        print(f"  • {agent_config['name']}: http://localhost:{agent_config['port']}")
    
    print("\n💡 To deploy to AgentVerse, run:")
    print("   python deployment/deploy_agents.py")
    
    print("\n🛑 Press Ctrl+C to stop all agents")
    
    # Keep the script running and monitor agents
    try:
        while True:
            time.sleep(10)
            
            # Check agent health
            for agent_config in started_agents:
                if not check_agent_health(agent_config):
                    print(f"⚠️  {agent_config['name']} may not be responding properly")
            
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
