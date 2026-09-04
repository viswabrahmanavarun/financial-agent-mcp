from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent import FinancialAgent, PERSONAS
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Financial Agent API")

# Initialize agent once (it will spawn short-lived MCP client sessions per request)
agent = FinancialAgent()

class QueryRequest(BaseModel):
    query: str
    persona: str
    sector: str

class QueryResponse(BaseModel):
    answer: str
    persona_used: str
    sector_context: str

@app.post("/query", response_model=QueryResponse)
async def query_agent(req: QueryRequest):
    if req.persona not in PERSONAS:
        raise HTTPException(status_code=400, detail=f"Invalid persona. Must be one of: {list(PERSONAS.keys())}")
        
    try:
        answer = await agent.query(req.query, req.persona, req.sector)
        return QueryResponse(
            answer=answer,
            persona_used=req.persona,
            sector_context=req.sector
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
