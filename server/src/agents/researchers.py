import os
import sys
import yaml
import json
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from crewai.llm import LLM
from serpapi import GoogleSearch

# Load environment variables
load_dotenv()

# Import your own path
module_dir = os.path.abspath('C:\Users\Anirudh\Documents\myapps\rockefeller\server\src\models') 
sys.path.insert(0, module_dir)
from research_output import MarketResearchOutput, TargetCustomerProfile, MarketPositioning, BrandingProtocol

class SearchTool(BaseTool):
    name: str = "search"
    description: str = "Search for market information, competitor data, and consumer insights."

    def _run(self, query: str) -> str:
        try: 
            search = GoogleSearch({
                "q": query,
                "api_key": os.environ.get("SERPER_API_KEY", "")
            })
            results = search.get_dict()
            
            if "organic_results" in results:
                return str(results["organic_results"][:3])
            return "No search results found"
        except Exception as e: 
            return f"Search error: {e}"

class MarketResearchCrew:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.agents_config_path = os.path.join(current_dir, 'config', 'research_agents.yaml')
        self.tasks_config_path = os.path.join(current_dir, 'config', 'research_tasks.yaml')
        
        self.agents_config = self.load_config(self.agents_config_path)
        self.tasks_config = self.load_config(self.tasks_config_path)
        self.llm = self.create_openai_llm()
        self.search_tool = SearchTool()

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load YAML configuration file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading config {config_path}: {e}")
            return {}

    def create_openai_llm(self) -> LLM:
        api_key = os.environ.get("OPENAI_API_KEY")

        return LLM(
            model="gpt-4o",
            api_key=api_key
        )

    def create_agent(self, agent_name: str, business_idea: str) -> Agent:
        config = self.agents_config.get(agent_name, {})
        return Agent(
            role=config.get("role", ""),
            goal=config.get("goal", "").format(business_idea=business_idea),
            backstory=config.get("backstory", "").format(business_idea=business_idea),
            llm=self.llm,
            max_iter=config.get("max_iter", 2),
            memory=config.get("memory", False),
            allow_delegation=config.get("allow_delegation", False),
            tools=[self.search_tool]
        )

    def create_manager_agent(self, agent_name: str, business_idea: str) -> Agent:
        """Create manager agent without tools for hierarchical processing"""
        config = self.agents_config.get(agent_name, {})
        return Agent(
            role=config.get("role", ""),
            goal=config.get("goal", "").format(business_idea=business_idea),
            backstory=config.get("backstory", "").format(business_idea=business_idea),
            llm=self.llm,
            max_iter=config.get("max_iter", 1),
            memory=config.get("memory", False),
            allow_delegation=config.get("allow_delegation", True),
            # No tools for manager agent
        )

    def create_task(self, task_name: str, business_idea: str, agent: Agent) -> Task:
        config = self.tasks_config.get(task_name, {})
        return Task(
            description=config.get("description", "").format(business_idea=business_idea),
            expected_output=config.get("expected_output", ""),
            agent=agent
        )

    def create_crew(self, business_idea: str) -> Crew:
        # Create sub-agents (with tools)
        market_analyst = self.create_agent("market_analyst", business_idea)
        consumer_psychologist = self.create_agent("consumer_psychologist", business_idea)
        cultural_strategist = self.create_agent("cultural_strategist", business_idea)
        
        # Create manager agent (without tools)
        synthesizer = self.create_manager_agent("synthesizer", business_idea)
        
        # Create tasks
        market_task = self.create_task("market_analysis", business_idea, market_analyst)
        consumer_task = self.create_task("consumer_profiling", business_idea, consumer_psychologist)
        brand_task = self.create_task("brand_guidelines", business_idea, cultural_strategist)
        synthesis_task = self.create_task("branding_synthesis", business_idea, synthesizer)
        
        return Crew(
            agents=[market_analyst, consumer_psychologist, cultural_strategist],
            tasks=[market_task, consumer_task, brand_task, synthesis_task],
            process=Process.hierarchical,
            manager_agent=synthesizer,
            verbose=True
        )

    def research(self, business_idea: str) -> MarketResearchOutput:
        """Conduct research and return structured output"""
        try: 
            crew = self.create_crew(business_idea)
            result = crew.kickoff()
            result_text = str(result)
            
            os.makedirs('output', exist_ok=True)
            with open('output/research.txt', 'w') as f:
                f.write(result_text)
            
            output = MarketResearchOutput(
                business_idea=business_idea,
                target_customer_profile=TargetCustomerProfile(
                    demographics=result_text,
                    psychographics=result_text,
                    buying_motivators=result_text
                ),
                market_positioning=MarketPositioning(
                    landscape_summary=result_text,
                    unique_value_proposition=result_text,
                    recommended_tone_style=result_text
                ),
                branding_protocol=BrandingProtocol(
                    visual_identity=result_text,
                    tone_voice=result_text,
                    cultural_guidelines=result_text,
                    competitive_differentiation=result_text
                ),
                timestamp=datetime.now()
            )
            
            # Save JSON output
            with open('output/research.json', 'w') as f:
                json.dump(output.dict(), f, indent=2, default=str)
            
            return output
        
        except Exception as e: 
            print(f"Research error: {e}")
            return MarketResearchOutput(
                business_idea=business_idea,
                target_customer_profile=TargetCustomerProfile(
                    demographics="",
                    psychographics="",
                    buying_motivators=""
                ),
                market_positioning=MarketPositioning(
                    landscape_summary="",
                    unique_value_proposition="",
                    recommended_tone_style=""
                ),
                branding_protocol=BrandingProtocol(
                    visual_identity="",
                    tone_voice="",
                    cultural_guidelines="",
                    competitive_differentiation=""
                ),
                timestamp=datetime.now()
            )

if __name__ == "__main__":
    business_idea = """Urban Paws Supply, based in Brooklyn, New York, is an online store that curates stylish,
                       eco-friendly pet accessories — like biodegradable poop bags, organic treats, and durable leashes made 
                       from recycled materials. The goal is to blend sustainability with modern pet ownership, targeting young 
                       urban professionals who see pets as part of their lifestyle."""
    
    print(f"🚀 Starting market research for: {business_idea}")
    print("=" * 70)
    
    crew = MarketResearchCrew()
    result = crew.research(business_idea)
    
    print(f"\n✅ Research completed!")
    print(f"📄 Text output saved to: research.txt")
    print(f"📊 JSON output saved to: research.json")
    print(f"⏰ Timestamp: {result.timestamp}")