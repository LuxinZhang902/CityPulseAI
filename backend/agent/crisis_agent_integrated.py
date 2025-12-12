"""CityPulse AI Crisis Intelligence Agent - Integrated with SnowLeopard Playground."""
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from .snowleopard_client_integrated import SnowLeopardClient

class CityPulseAgent:
    """
    Advanced multi-signal crisis intelligence agent with integrated SnowLeopard Playground.
    
    Workflow: planner → SQL generator → validator → analyst → storyteller → map generator
    """
    
    def __init__(self, db_path: str, snowleopard_api_key: Optional[str] = None, use_playground: bool = True, datafile_id: Optional[str] = None):
        self.db_path = db_path
        self.snowleopard = SnowLeopardClient(
            api_key=snowleopard_api_key,
            use_playground=use_playground,
            datafile_id=datafile_id
        )
        self.schema = self._load_schema()
        
        print(f"🐾 CityPulse Agent initialized with SnowLeopard mode: {self.snowleopard.get_mode()}")
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load database schema for SnowLeopard."""
        return {
            "tables": [
                {
                    "name": "sf_police_calls_rt",
                    "columns": ["cad_id", "received_datetime", "dispatch_datetime", 
                               "closed_datetime", "call_type", "priority", "disposition",
                               "neighborhood", "latitude", "longitude"]
                },
                {
                    "name": "sf_fire_ems_calls",
                    "columns": ["call_number", "incident_number", "received_datetime",
                               "dispatch_datetime", "unit_id", "call_type", "disposition",
                               "neighborhood", "latitude", "longitude"]
                },
                {
                    "name": "sf_311_cases",
                    "columns": ["case_id", "opened_datetime", "closed_datetime", "status",
                               "category", "subcategory", "neighborhood", "latitude", "longitude"]
                },
                {
                    "name": "sf_shelter_waitlist",
                    "columns": ["record_id", "snapshot_date", "neighborhood", 
                               "people_waiting", "shelter_type"]
                },
                {
                    "name": "sf_homeless_baseline",
                    "columns": ["neighborhood", "unsheltered_count", "sheltered_count", "snapshot_year"]
                },
                {
                    "name": "sf_disaster_events",
                    "columns": ["event_id", "event_type", "description", "timestamp",
                               "latitude", "longitude", "neighborhood", "severity", "source"]
                },
                {
                    "name": "neighborhoods",
                    "columns": ["name", "population", "seniors_65_plus"]
                }
            ]
        }
    
    def analyze(self, question: str) -> Dict[str, Any]:
        """
        Main agent entry point with integrated SnowLeopard Playground.
        
        Args:
            question: Natural language query about SF emergencies/crises
            
        Returns:
            Structured analysis with metrics, insights, map layers, and SQL
        """
        # Step 1: Interpret intent
        intent = self._interpret_intent(question)
        
        # Step 2: Plan SQL strategy
        strategy = self._plan_strategy(intent, question)
        
        # Step 3: Generate SQL using integrated SnowLeopard
        sql_result = self.snowleopard.generate_sql(
            question=question,
            schema=self.schema,
            context=strategy["context"]
        )
        
        # Add source information to results
        sql_result["source"] = getattr(self.snowleopard, 'get_mode', lambda: 'unknown')()
        
        # Step 4: Execute SQL
        try:
            raw_data = self._execute_sql(sql_result["sql"])
        except Exception as e:
            # Step 4b: Retry with corrected SQL if needed
            return {
                "error": f"SQL execution failed: {str(e)}",
                "sql_used": sql_result["sql"],
                "source": sql_result.get("source", "unknown"),
                "suggestion": "Please rephrase your question or check database contents"
            }
        
        # Step 5: Compute scores and analyze
        analysis = self._analyze_results(raw_data, intent)
        
        # Step 6: Generate insights
        insights = self._generate_insights(analysis, raw_data, intent)
        
        # Step 7: Create map layers
        map_layers = self._create_map_layers(raw_data, intent)
        
        # Step 8: Format final output
        return {
            "analysis_type": intent["type"],
            "timestamp": datetime.utcnow().isoformat(),
            "top_neighborhoods": analysis["top_neighborhoods"],
            "insight_summary": insights,
            "map_layers": map_layers,
            "sql_used": sql_result["sql"],
            "sql_source": sql_result.get("source", "unknown"),
            "sql_explanation": sql_result.get("explanation", ""),
            "raw_rows": raw_data[:20]  # Limit to first 20 rows
        }
    
    def _interpret_intent(self, question: str) -> Dict[str, str]:
        """Determine query intent."""
        question_lower = question.lower()
        
        if "emergency" in question_lower and "stress" in question_lower:
            return {"type": "emergency_stress", "timeframe": "24h"}
        elif "homeless" in question_lower or "shelter" in question_lower:
            return {"type": "homelessness_pressure", "timeframe": "7d"}
        elif "disaster" in question_lower or "earthquake" in question_lower or "fire" in question_lower:
            return {"type": "disaster_impact", "timeframe": "6h"}
        else:
            return {"type": "mixed_query", "timeframe": "24h"}
    
    def _plan_strategy(self, intent: Dict[str, str], question: str) -> Dict[str, Any]:
        """Plan SQL generation strategy."""
        strategy = {
            "tables": [],
            "metrics": [],
            "grouping": "neighborhood",
            "context": ""
        }
        
        if intent["type"] == "emergency_stress":
            strategy["tables"] = ["sf_police_calls_rt", "sf_fire_ems_calls"]
            strategy["metrics"] = ["police_calls", "fire_ems_calls", "stress_score"]
            strategy["context"] = f"Focus on past {intent['timeframe']}. Compute stress score as: police_calls * 1.0 + fire_ems_calls * 1.2"
        
        elif intent["type"] == "homelessness_pressure":
            strategy["tables"] = ["sf_shelter_waitlist", "sf_homeless_baseline"]
            strategy["metrics"] = ["people_waiting", "pressure_ratio"]
            strategy["context"] = f"Focus on past {intent['timeframe']}. Calculate pressure as waitlist / shelter capacity"
        
        elif intent["type"] == "disaster_impact":
            strategy["tables"] = ["sf_disaster_events"]
            strategy["metrics"] = ["event_count", "severity"]
            strategy["context"] = f"Focus on past {intent['timeframe']}. Group by event type and neighborhood"
        
        return strategy
    
    def _execute_sql(self, sql: str) -> List[Dict[str, Any]]:
        """Execute SQL against SQLite database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        # Convert to list of dicts
        result = [dict(row) for row in rows]
        
        conn.close()
        return result
    
    def _analyze_results(self, data: List[Dict[str, Any]], intent: Dict[str, str]) -> Dict[str, Any]:
        """Compute scores and rankings."""
        if not data:
            return {"top_neighborhoods": [], "total_incidents": 0}
        
        # Extract top neighborhoods
        top_neighborhoods = []
        for row in data[:10]:
            neighborhood_data = {
                "name": row.get("neighborhood", "Unknown"),
                "metrics": {}
            }
            
            # Add all numeric metrics
            for key, value in row.items():
                if key != "neighborhood" and isinstance(value, (int, float)):
                    neighborhood_data["metrics"][key] = value
            
            top_neighborhoods.append(neighborhood_data)
        
        return {
            "top_neighborhoods": top_neighborhoods,
            "total_incidents": len(data)
        }
    
    def _generate_insights(
        self,
        analysis: Dict[str, Any],
        raw_data: List[Dict[str, Any]],
        intent: Dict[str, str]
    ) -> str:
        """Generate AI insights from data."""
        if not analysis["top_neighborhoods"]:
            return "No significant activity detected in the specified timeframe."
        
        top = analysis["top_neighborhoods"][0]
        insights = []
        
        # Identify hotspot
        insights.append(f"🔴 **{top['name']}** is the highest-stress neighborhood")
        
        # Detect anomalies
        if len(analysis["top_neighborhoods"]) > 1:
            second = analysis["top_neighborhoods"][1]
            if "stress_score" in top["metrics"] and "stress_score" in second["metrics"]:
                diff_pct = ((top["metrics"]["stress_score"] - second["metrics"]["stress_score"]) 
                           / second["metrics"]["stress_score"] * 100)
                if diff_pct > 30:
                    insights.append(f"⚠️ {diff_pct:.0f}% higher stress than second-ranked neighborhood")
        
        # Suggest actions
        if intent["type"] == "emergency_stress":
            insights.append(f"💡 Deploy additional EMS resources to {top['name']}")
        elif intent["type"] == "homelessness_pressure":
            insights.append(f"💡 Increase shelter capacity in {top['name']}")
        elif intent["type"] == "disaster_impact":
            insights.append(f"💡 Activate emergency response protocols in {top['name']}")
        
        return " | ".join(insights)
    
    def _create_map_layers(
        self,
        data: List[Dict[str, Any]],
        intent: Dict[str, str]
    ) -> Dict[str, Any]:
        """Generate map-ready JSON for Google Maps/Mapbox."""
        heatmap_data = []
        markers = []
        
        for row in data:
            lat = row.get("latitude")
            lon = row.get("longitude")
            
            if lat and lon:
                # Heatmap point
                weight = 1.0
                if "stress_score" in row:
                    weight = row["stress_score"] / 10.0
                elif "event_count" in row:
                    weight = row["event_count"] / 5.0
                
                heatmap_data.append({
                    "lat": lat,
                    "lng": lon,
                    "weight": weight
                })
                
                # Marker
                markers.append({
                    "lat": lat,
                    "lng": lon,
                    "title": row.get("neighborhood", "Unknown"),
                    "description": self._format_marker_description(row),
                    "severity": self._determine_severity(row)
                })
        
        return {
            "heatmap": heatmap_data,
            "markers": markers,
            "center": {"lat": 37.7749, "lng": -122.4194},  # SF center
            "zoom": 12
        }
    
    def _format_marker_description(self, row: Dict[str, Any]) -> str:
        """Format marker popup description."""
        parts = []
        for key, value in row.items():
            if key not in ["latitude", "longitude", "neighborhood"]:
                parts.append(f"{key}: {value}")
        return " | ".join(parts[:3])  # Limit to 3 metrics
    
    def _determine_severity(self, row: Dict[str, Any]) -> str:
        """Determine severity level for marker color."""
        if "stress_score" in row:
            score = row["stress_score"]
            if score > 20:
                return "critical"
            elif score > 10:
                return "high"
            else:
                return "medium"
        elif "severity" in row:
            return row["severity"].lower()
        else:
            return "low"
    
    def switch_mode(self, mode: str, datafile_id: Optional[str] = None):
        """Switch between Playground and Direct API modes."""
        if mode.lower() == "playground":
            self.snowleopard.switch_to_playground(datafile_id)
        elif mode.lower() == "direct":
            self.snowleopard.switch_to_direct_api()
        else:
            print(f"❌ Unknown mode: {mode}. Use 'playground' or 'direct'")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "snowleopard_mode": self.snowleopard.get_mode(),
            "database_path": self.db_path,
            "tables_count": len(self.schema["tables"]),
            "api_key_configured": bool(self.snowleopard.api_key)
        }
