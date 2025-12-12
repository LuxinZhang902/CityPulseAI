"""FastAPI backend for CityPulse AI."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import os
from agent import CityPulseAgent

app = FastAPI(
    title="CityPulse AI",
    description="Real-Time Urban Crisis Intelligence Agent",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
DB_PATH = Path(__file__).parent.parent / "database" / "citypulse.db"
SNOWLEOPARD_API_KEY = os.getenv("SNOWLEOPARD_API_KEY")

agent = CityPulseAgent(
    db_path=str(DB_PATH),
    snowleopard_api_key=SNOWLEOPARD_API_KEY
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    analysis_type: str
    timestamp: str
    top_neighborhoods: list
    insight_summary: str
    map_layers: dict
    sql_used: str
    raw_rows: list

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "CityPulse AI",
        "status": "operational",
        "version": "1.0.0"
    }

@app.post("/api/analyze", response_model=QueryResponse)
async def analyze_crisis(request: QueryRequest):
    """
    Analyze urban crisis using natural language query.
    
    Examples:
    - "Where is SF under the highest emergency stress right now?"
    - "Which neighborhoods show rising homelessness pressure this week?"
    - "An earthquake hit an hour ago—who is most impacted?"
    """
    try:
        result = agent.analyze(request.question)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/schema")
async def get_schema():
    """Get database schema information."""
    return agent.schema

@app.get("/api/health")
async def health_check():
    """Check database connectivity and agent status."""
    try:
        # Test database connection
        test_result = agent._execute_sql("SELECT 1")
        return {
            "database": "connected",
            "agent": "ready",
            "snowleopard": "configured" if SNOWLEOPARD_API_KEY else "fallback_mode"
        }
    except Exception as e:
        return {
            "database": "error",
            "agent": "degraded",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
