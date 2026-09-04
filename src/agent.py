import asyncio
import os
import json
from google import genai
from google.genai import types

# Import the tool functions directly from our MCP server file
from src.mcp_server import (
    get_companies_by_sector,
    get_company_financials,
    get_company_operational_metrics,
    search_all_data_for_sector
)

# Define Personas
PERSONAS = {
    "Mutual Fund Analyst": "You are a Mutual Fund Analyst. You have a long-only, benchmark-relative focus. You care deeply about sustainable growth, valuation versus the index (e.g., S&P 500, NASDAQ), and how a company fits into a core portfolio holding. Do not focus on short-term trading or aggressive leverage.",
    "Equity Analyst": "You are an Equity Analyst. You are highly fundamentals-driven. When analyzing companies, focus heavily on earnings trends, profit margins, competitive positioning within the sector, and valuation multiples to derive price targets.",
    "PE Analyst": "You are a Private Equity (PE) Analyst. You view everything through a deal/ops lens. Focus on cash flow generation, leverage capacity (debt-to-equity), operational improvement levers, entry multiples, and exit potential. You are looking for buyout targets to take private."
}

class FinancialAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=self.api_key)
        
        # Tools we expose to Gemini (directly mapped to our MCP functions)
        self.tools = [
            get_companies_by_sector,
            get_company_financials,
            get_company_operational_metrics,
            search_all_data_for_sector
        ]

    async def query(self, user_query: str, persona: str, sector: str) -> str:
        """Main method to query the agent."""
        if persona not in PERSONAS:
            raise ValueError(f"Invalid persona: {persona}")
            
        system_instruction = f"{PERSONAS[persona]}\n\nThe user is asking about the '{sector}' sector. You MUST use your tools to fetch data from the database. NEVER hardcode facts or hallucinate companies not in the database. If asked about a company not in the dataset, clearly state you have no data on it. Ground your answer strictly in the data retrieved."
        
        chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                tools=self.tools
            )
        )
        
        # Send user query and let Gemini automatically call the Python functions
        response = chat.send_message(user_query)
        
        return response.text

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    agent = FinancialAgent()
    
    # Test query
    async def run_test():
        print("Testing PE Analyst...")
        res = await agent.query("Which companies in this sector look like attractive buyout targets?", "PE Analyst", "Tech")
        print(res)
        
    asyncio.run(run_test())
