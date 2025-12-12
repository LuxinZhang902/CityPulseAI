"""SnowLeopard.ai SQL generation client."""
import os
import requests
from typing import Dict, Any, Optional

class SnowLeopardClient:
    """Client for SnowLeopard.ai SQL generation API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SNOWLEOPARD_API_KEY")
        self.base_url = "https://api.snowleopard.ai/v1"
        
    def generate_sql(
        self,
        question: str,
        schema: Dict[str, Any],
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate SQL query using SnowLeopard.ai.
        
        Args:
            question: Natural language question
            schema: Database schema information
            context: Additional context for query generation
            
        Returns:
            Dict with 'sql', 'explanation', and 'confidence'
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "question": question,
            "schema": schema,
            "dialect": "sqlite",
            "context": context
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/generate-sql",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Fallback to local SQL generation if API fails
            return self._fallback_sql_generation(question, schema)
    
    def _fallback_sql_generation(
        self,
        question: str,
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback SQL generation when SnowLeopard API is unavailable.
        Uses rule-based approach for common query patterns.
        """
        question_lower = question.lower()
        
        # Emergency stress query
        if "emergency" in question_lower and "stress" in question_lower:
            sql = """
            SELECT 
                COALESCE(p.neighborhood, f.neighborhood) as neighborhood,
                COUNT(DISTINCT p.cad_id) as police_calls,
                COUNT(DISTINCT f.call_number) as fire_ems_calls,
                (COUNT(DISTINCT p.cad_id) * 1.0 + COUNT(DISTINCT f.call_number) * 1.2) as stress_score,
                AVG(p.latitude) as latitude,
                AVG(p.longitude) as longitude
            FROM sf_police_calls_rt p
            FULL OUTER JOIN sf_fire_ems_calls f 
                ON p.neighborhood = f.neighborhood
            WHERE datetime(p.received_datetime) >= datetime('now', '-24 hours')
                OR datetime(f.received_datetime) >= datetime('now', '-24 hours')
            GROUP BY COALESCE(p.neighborhood, f.neighborhood)
            ORDER BY stress_score DESC
            LIMIT 10
            """
            return {
                "sql": sql,
                "explanation": "Emergency stress analysis for past 24 hours",
                "confidence": 0.85
            }
        
        # Homelessness pressure query
        elif "homeless" in question_lower or "shelter" in question_lower:
            sql = """
            SELECT 
                s.neighborhood,
                SUM(s.people_waiting) as total_waiting,
                h.unsheltered_count,
                h.sheltered_count,
                (SUM(s.people_waiting) * 1.0 / NULLIF(h.sheltered_count, 0)) as pressure_ratio
            FROM sf_shelter_waitlist s
            LEFT JOIN sf_homeless_baseline h ON s.neighborhood = h.neighborhood
            WHERE date(s.snapshot_date) >= date('now', '-7 days')
            GROUP BY s.neighborhood
            ORDER BY pressure_ratio DESC
            LIMIT 10
            """
            return {
                "sql": sql,
                "explanation": "Homelessness pressure analysis for past 7 days",
                "confidence": 0.80
            }
        
        # Disaster impact query
        elif "disaster" in question_lower or "earthquake" in question_lower:
            sql = """
            SELECT 
                neighborhood,
                event_type,
                COUNT(*) as event_count,
                severity,
                MAX(timestamp) as latest_event,
                AVG(latitude) as latitude,
                AVG(longitude) as longitude
            FROM sf_disaster_events
            WHERE datetime(timestamp) >= datetime('now', '-6 hours')
            GROUP BY neighborhood, event_type
            ORDER BY event_count DESC, severity DESC
            LIMIT 10
            """
            return {
                "sql": sql,
                "explanation": "Disaster impact analysis for past 6 hours",
                "confidence": 0.90
            }
        
        # Default: general neighborhood stress
        else:
            sql = """
            SELECT 
                neighborhood,
                COUNT(*) as total_incidents,
                call_type,
                AVG(latitude) as latitude,
                AVG(longitude) as longitude
            FROM (
                SELECT neighborhood, call_type, latitude, longitude, received_datetime
                FROM sf_police_calls_rt
                UNION ALL
                SELECT neighborhood, call_type, latitude, longitude, received_datetime
                FROM sf_fire_ems_calls
            )
            WHERE datetime(received_datetime) >= datetime('now', '-24 hours')
            GROUP BY neighborhood
            ORDER BY total_incidents DESC
            LIMIT 10
            """
            return {
                "sql": sql,
                "explanation": "General incident analysis for past 24 hours",
                "confidence": 0.75
            }
