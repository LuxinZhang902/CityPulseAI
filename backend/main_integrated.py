"""FastAPI backend for CityPulse AI - Integrated with SnowLeopard Playground."""
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Dict, Any, Optional
import uvicorn
import os
from datetime import datetime
from pathlib import Path
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Import our integrated agent
from agent.crisis_agent_integrated import CityPulseAgent
from services.pdf_generator import pdf_generator
from services.realtime_sync import RealtimeDataSync

app = FastAPI(
    title="CityPulse AI - Integrated",
    description="Real-Time Urban Crisis Intelligence Agent with SnowLeopard Playground Integration",
    version="2.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize integrated agent
DB_PATH = Path(__file__).parent.parent / "database" / "citypulse.db"
SNOWLEOPARD_API_KEY = os.getenv("SNOWLEOPARD_API_KEY")
USE_PLAYGROUND = os.getenv("USE_PLAYGROUND", "true").lower() == "true"
DATAFILE_ID = os.getenv("SNOWLEOPARD_DATAFILE_ID", "793f36afcd494309963477d7e7f4075b")
SYNC_ON_STARTUP = os.getenv("SYNC_REALTIME_DATA", "false").lower() == "true"

# Sync real-time data once at startup if enabled
if SYNC_ON_STARTUP:
    print("\n" + "="*60)
    print("🌐 Syncing Real-Time Data from SF Open Data APIs...")
    print("="*60)
    syncer = RealtimeDataSync(DB_PATH)
    try:
        syncer.sync_all()
        print("✅ Real-time data sync complete!")
    except Exception as e:
        print(f"⚠️  Real-time sync failed: {e}")
        print("📊 Continuing with existing database data...")
    print("="*60 + "\n")

agent = CityPulseAgent(
    db_path=str(DB_PATH),
    snowleopard_api_key=SNOWLEOPARD_API_KEY,
    use_playground=USE_PLAYGROUND,
    datafile_id=DATAFILE_ID
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    query: str
    analysis_type: str
    intent: Dict[str, str]
    insight_summary: str
    key_insights: list
    risk_level: Optional[str] = None
    recommendations: Optional[list] = None
    top_neighborhoods: list
    raw_rows: list
    sql_used: str
    sql_explanation: str
    sql_source: str
    map_layers: Dict[str, Any]
    chart_data: Optional[Dict[str, Any]] = None
    confidence: float
    snowleopard_solution: bool
    technical_details: Optional[str] = None
    comprehensive_analysis: Optional[Dict[str, Any]] = None
    timestamp: str

class ModeRequest(BaseModel):
    mode: str  # "playground" or "direct"
    datafile_id: str = None

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "CityPulse AI - Integrated",
        "status": "operational",
        "version": "2.0.0",
        "snowleopard_mode": agent.get_status()["snowleopard_mode"]
    }

@app.post("/api/analyze", response_model=QueryResponse)
async def analyze_crisis(request: QueryRequest):
    """
    Analyze urban crisis using natural language query with integrated SnowLeopard.
    
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

@app.post("/api/switch-mode")
async def switch_mode(request: ModeRequest):
    """Switch between Playground and Direct API modes."""
    try:
        agent.switch_mode(request.mode, request.datafile_id)
        return {
            "message": f"Switched to {request.mode} mode",
            "current_mode": agent.get_status()["snowleopard_mode"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_status():
    """Get detailed agent status."""
    return agent.get_status()

@app.get("/api/schema")
async def get_schema():
    """Get database schema information."""
    return agent.schema

@app.post("/api/generate-pdf")
async def generate_pdf_report(request: QueryRequest):
    """Generate a comprehensive PDF report for the analysis."""
    try:
        # First, get the analysis data
        result = agent.analyze(request.question)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Generate PDF report
        pdf_path = pdf_generator.generate_report(result)
        
        # Return the PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=os.path.basename(pdf_path)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Check database connectivity and agent status."""
    try:
        # Test database connection
        test_result = agent._execute_sql("SELECT 1")
        status = agent.get_status()
        return {
            "database": "connected",
            "agent": "ready",
            "snowleopard": status["snowleopard_mode"],
            "api_key_configured": status["api_key_configured"],
            "datafile_id": DATAFILE_ID if USE_PLAYGROUND else None
        }
    except Exception as e:
        return {
            "database": "error",
            "agent": "degraded",
            "error": str(e)
        }

@app.get("/api/demo-queries")
async def get_demo_queries():
    """Get list of demo queries for testing."""
    return {
        "queries": [
            "How many police calls are in the database?",
            "Which neighborhood has the most fire/EMS calls?",
            "Show me all disaster events in the past 24 hours",
            "What is the total number of 311 cases?",
            "Which neighborhoods have the highest shelter waitlist counts?",
            "Count the number of incidents by call type in Tenderloin",
            "What are the top 5 neighborhoods with the most emergency calls?",
            "Show me all hazmat incidents with their severity levels",
            "How many neighborhoods are in the database?",
            "What is the stress score for each neighborhood (police calls + 1.2 * fire calls)?"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
