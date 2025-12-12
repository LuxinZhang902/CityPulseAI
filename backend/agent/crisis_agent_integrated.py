"""CityPulse AI Crisis Intelligence Agent - Integrated with SnowLeopard Playground."""
import sqlite3
import time
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
        print("🚀 Starting CityPulse analysis...")
        print(f"❓ Question: {question}")
        start_time = time.time()
        
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
        
        # Step 4: Use SnowLeopard's solution if available, otherwise execute locally
        if sql_result.get("has_solution") and sql_result.get("data"):
            # Use SnowLeopard's complete solution if available
            print("✅ Using SnowLeopard's complete solution (SQL + Data + Analysis)")
            
            # Extract data from SnowLeopard result
            raw_rows = sql_result.get('rows', [])
            analysis = sql_result.get('analysis', {})
            
            # Check if this is insurance mode
            if intent["type"] == "insurance_report":
                print("🏢 Processing Insurance Underwriting Report...")
                return self._generate_insurance_report(question, raw_rows, sql_result, intent)
            
            # Generate insights using SnowLeopard analysis
            insight_summary = analysis.get('executive_summary', 'Analysis completed using SnowLeopard AI')
            key_insights = analysis.get('key_insights', ['Data processed successfully'])
            risk_level = analysis.get('risk_assessment', {}).get('level', 'medium')
            recommendations = analysis.get('recommendations', [])
            
            # Create top neighborhoods from SnowLeopard data
            top_neighborhoods = self._create_neighborhood_rankings(raw_rows)
            
            # Generate map layers from SnowLeopard data
            map_layers = self._create_map_layers(raw_rows, intent)
            
            # Create chart data from SnowLeopard suggestions
            chart_data = self._generate_chart_data(raw_rows, analysis.get('chart_suggestions', []))
            
            # Determine analysis type based on query and data
            analysis_type = self._determine_analysis_type(question, raw_rows)
            
            # Enhanced SQL source string
            sql_source = f"Playground (datafile: {self.snowleopard.datafile_id}) (with complete SnowLeopard analysis)"
            
            final_response = {
                'query': question,
                'analysis_type': analysis_type,
                'intent': intent,
                'insight_summary': insight_summary,
                'key_insights': key_insights,
                'risk_level': risk_level,
                'recommendations': recommendations,
                'top_neighborhoods': top_neighborhoods,
                'raw_rows': raw_rows,
                'sql_used': sql_result['sql'],
                'sql_explanation': sql_result.get('explanation', 'Generated by SnowLeopard AI'),
                'sql_source': sql_source,
                'map_layers': map_layers,
                'chart_data': chart_data,
                'confidence': sql_result.get('confidence', 0.9),
                'snowleopard_solution': True,
                'technical_details': sql_result.get('technical_details', ''),
                'comprehensive_analysis': analysis
            }
            
            end_time = time.time()
            total_time = end_time - start_time
            print(f"🎯 Complete SnowLeopard solution generated in {total_time:.2f} seconds!")
            print(f"📊 Returned {len(raw_rows)} rows of data")
            print(f"🧠 Analysis type: {analysis_type}")
            print(f"🗺️ Generated {len(map_layers)} map layers")
            
            return final_response
        else:
            # Execute SQL locally (fallback)
            try:
                raw_data = self._execute_sql(sql_result["sql"])
                sql_source = sql_result.get("source", "unknown")
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
            "query": question,
            "analysis_type": intent["type"],
            "intent": intent,
            "timestamp": datetime.utcnow().isoformat(),
            "top_neighborhoods": analysis["top_neighborhoods"],
            "insight_summary": insights,
            "key_insights": [insights],  # Wrap in list for consistency
            "map_layers": map_layers,
            "sql_used": sql_result["sql"],
            "sql_source": sql_source,  # Use enhanced source info
            "sql_explanation": sql_result.get("explanation", ""),
            "technical_details": sql_result.get("technical_details", ""),
            "confidence": sql_result.get("confidence", 0.7),
            "snowleopard_solution": sql_result.get("has_solution", False),
            "raw_rows": raw_data[:20]  # Limit to first 20 rows
        }
    
    def _interpret_intent(self, question: str) -> Dict[str, str]:
        """Determine query intent."""
        question_lower = question.lower()
        
        # Insurance Report Mode triggers
        insurance_keywords = ["insurance", "underwriting", "claims risk", "portfolio risk", 
                             "exposure", "catastrophe report", "insurer", "reinsurer", "underwriter"]
        if any(keyword in question_lower for keyword in insurance_keywords):
            return {"type": "insurance_report", "timeframe": "7d"}
        
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
        
        if intent["type"] == "insurance_report":
            strategy["tables"] = ["sf_disaster_events", "sf_311_cases", "sf_fire_ems_calls", "sf_police_calls_rt"]
            strategy["metrics"] = ["earthquake_events", "avg_quake_severity", "fire_events", "hazmat_events", 
                                  "infra_311_cases", "ems_calls", "police_calls"]
            strategy["context"] = f"""
            INSURANCE UNDERWRITING MODE - Generate SQL for risk assessment:
            
            Required columns per neighborhood (within past {intent['timeframe']}):
            - neighborhood
            - earthquake_events (COUNT from sf_disaster_events WHERE event_type='earthquake')
            - avg_quake_severity (AVG severity for earthquakes)
            - fire_events (COUNT from sf_disaster_events WHERE event_type='fire')
            - hazmat_events (COUNT from sf_disaster_events WHERE event_type='hazmat')
            - infra_311_cases (COUNT from sf_311_cases for infrastructure issues)
            - ems_calls (COUNT from sf_fire_ems_calls)
            - police_calls (COUNT from sf_police_calls_rt)
            - latitude, longitude (AVG for mapping)
            
            Join tables on neighborhood. Include only neighborhoods with data.
            Time filter: past {intent['timeframe']} using received_datetime or event_datetime.
            """
        
        elif intent["type"] == "emergency_stress":
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
    
    def _generate_insurance_report(self, question: str, raw_rows: List[Dict], sql_result: Dict, intent: Dict) -> Dict[str, Any]:
        """Generate insurance underwriting report with risk scoring."""
        print("📊 Computing insurance risk scores...")
        
        # Calculate risk scores for each neighborhood
        scored_neighborhoods = []
        for row in raw_rows:
            neighborhood = row.get('neighborhood', 'Unknown')
            
            # Extract metrics (with defaults)
            earthquake_events = row.get('earthquake_events', 0) or 0
            avg_quake_severity = row.get('avg_quake_severity', 0) or 0
            fire_events = row.get('fire_events', 0) or 0
            hazmat_events = row.get('hazmat_events', 0) or 0
            infra_311_cases = row.get('infra_311_cases', 0) or 0
            ems_calls = row.get('ems_calls', 0) or 0
            police_calls = row.get('police_calls', 0) or 0
            
            # Compute risk score using insurance formula
            risk_score = (
                12 * avg_quake_severity +
                10 * fire_events +
                12 * hazmat_events +
                2 * infra_311_cases +
                0.4 * (ems_calls + police_calls)
            )
            
            # Clamp to [0, 100]
            risk_score = max(0, min(100, risk_score))
            
            # Determine risk tier
            if risk_score >= 76:
                risk_tier = "Critical"
            elif risk_score >= 51:
                risk_tier = "High"
            elif risk_score >= 26:
                risk_tier = "Medium"
            else:
                risk_tier = "Low"
            
            scored_neighborhoods.append({
                'neighborhood': neighborhood,
                'risk_score': round(risk_score, 2),
                'risk_tier': risk_tier,
                'earthquake_events': earthquake_events,
                'avg_quake_severity': round(avg_quake_severity, 2) if avg_quake_severity else 0,
                'fire_events': fire_events,
                'hazmat_events': hazmat_events,
                'infra_311_cases': infra_311_cases,
                'ems_calls': ems_calls,
                'police_calls': police_calls,
                'latitude': row.get('latitude'),
                'longitude': row.get('longitude')
            })
        
        # Sort by risk score
        scored_neighborhoods.sort(key=lambda x: x['risk_score'], reverse=True)
        
        # Identify top risk drivers
        top_drivers = []
        if scored_neighborhoods:
            top_neighborhood = scored_neighborhoods[0]
            if top_neighborhood['earthquake_events'] > 0:
                top_drivers.append(f"Seismic activity: {top_neighborhood['earthquake_events']} earthquakes (avg severity: {top_neighborhood['avg_quake_severity']})")
            if top_neighborhood['fire_events'] > 0:
                top_drivers.append(f"Fire incidents: {top_neighborhood['fire_events']} events")
            if top_neighborhood['hazmat_events'] > 0:
                top_drivers.append(f"Hazmat incidents: {top_neighborhood['hazmat_events']} events")
            if top_neighborhood['infra_311_cases'] > 50:
                top_drivers.append(f"Infrastructure stress: {top_neighborhood['infra_311_cases']} 311 cases")
            if top_neighborhood['ems_calls'] + top_neighborhood['police_calls'] > 100:
                total_emergency = top_neighborhood['ems_calls'] + top_neighborhood['police_calls']
                top_drivers.append(f"Emergency load: {total_emergency} total calls")
        
        # Generate underwriting recommendations
        recommendations = []
        if scored_neighborhoods:
            top_risk = scored_neighborhoods[0]
            if top_risk['risk_tier'] == 'Critical':
                recommendations.append("BINDING PAUSE: Suspend new policy issuance pending risk inspection")
                recommendations.append("PRICING ADJUSTMENT: Apply 25-40% rate increase for renewals")
                recommendations.append("INSPECTION TRIGGER: Mandatory property inspection for all policies")
            elif top_risk['risk_tier'] == 'High':
                recommendations.append("PRICING ADJUSTMENT: Apply 15-25% rate increase")
                recommendations.append("ENHANCED MONITORING: Flag for quarterly risk review")
                recommendations.append("INSPECTION TRIGGER: Sample 30% of properties for inspection")
            elif top_risk['risk_tier'] == 'Medium':
                recommendations.append("STANDARD PRICING: Apply 5-10% rate adjustment")
                recommendations.append("MONITORING: Include in standard quarterly review")
            else:
                recommendations.append("STANDARD UNDERWRITING: Proceed with normal pricing")
                recommendations.append("MONITORING: Annual review cycle")
        
        # Generate risk summary
        total_neighborhoods = len(scored_neighborhoods)
        critical_count = sum(1 for n in scored_neighborhoods if n['risk_tier'] == 'Critical')
        high_count = sum(1 for n in scored_neighborhoods if n['risk_tier'] == 'High')
        
        risk_summary = f"Insurance risk assessment for {total_neighborhoods} neighborhoods. "
        if critical_count > 0:
            risk_summary += f"{critical_count} neighborhoods at CRITICAL risk require immediate underwriting action. "
        if high_count > 0:
            risk_summary += f"{high_count} neighborhoods at HIGH risk warrant enhanced monitoring. "
        risk_summary += "Analysis based on seismic activity, fire incidents, hazmat events, infrastructure stress, and emergency call volume."
        
        # Create map layers for insurance visualization
        map_layers = {
            'markers': [],
            'polygons': [],
            'heatmap': [],
            'center': {'lat': 37.7749, 'lng': -122.4194},
            'zoom': 12
        }
        
        # Add markers for high-risk neighborhoods
        for neighborhood in scored_neighborhoods[:10]:  # Top 10
            if neighborhood['latitude'] and neighborhood['longitude']:
                severity = 'critical' if neighborhood['risk_tier'] == 'Critical' else \
                          'high' if neighborhood['risk_tier'] == 'High' else 'medium'
                
                map_layers['markers'].append({
                    'lat': neighborhood['latitude'],
                    'lng': neighborhood['longitude'],
                    'title': neighborhood['neighborhood'],
                    'description': f"Risk Score: {neighborhood['risk_score']} | Tier: {neighborhood['risk_tier']} | Earthquakes: {neighborhood['earthquake_events']} | Fires: {neighborhood['fire_events']}",
                    'severity': severity
                })
                
                # Add to heatmap
                map_layers['heatmap'].append({
                    'lat': neighborhood['latitude'],
                    'lng': neighborhood['longitude'],
                    'weight': neighborhood['risk_score']
                })
        
        # Generate chart data for insurance report
        chart_data = self._generate_insurance_charts(scored_neighborhoods)
        
        # Build final insurance report
        return {
            'query': question,
            'analysis_type': 'insurance_report',
            'intent': intent,
            'risk_summary': risk_summary,
            'risk_tier': scored_neighborhoods[0]['risk_tier'] if scored_neighborhoods else 'Unknown',
            'risk_score': scored_neighborhoods[0]['risk_score'] if scored_neighborhoods else 0,
            'top_drivers': top_drivers if top_drivers else ['Insufficient data for risk driver analysis'],
            'recommended_actions': recommendations,
            'insight_summary': risk_summary,
            'key_insights': top_drivers if top_drivers else ['No significant risk drivers identified'],
            'top_neighborhoods': scored_neighborhoods[:10],
            'map_layers': map_layers,
            'chart_data': chart_data,
            'sql_used': sql_result['sql'],
            'sql_explanation': sql_result.get('explanation', 'Insurance risk assessment query'),
            'sql_source': f"Playground (datafile: {self.snowleopard.datafile_id}) - Insurance Mode",
            'technical_details': sql_result.get('technical_details', ''),
            'confidence': sql_result.get('confidence', 0.9),
            'snowleopard_solution': True,
            'raw_rows': raw_rows,
            'timestamp': datetime.utcnow().isoformat(),
            'comprehensive_analysis': {
                'executive_summary': risk_summary,
                'key_insights': top_drivers,
                'risk_assessment': {
                    'level': scored_neighborhoods[0]['risk_tier'] if scored_neighborhoods else 'Unknown',
                    'reasoning': f"Based on analysis of {len(scored_neighborhoods)} neighborhoods using insurance risk scoring model"
                },
                'recommendations': recommendations
            }
        }
    
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
    
    def _generate_insurance_charts(self, scored_neighborhoods: List[Dict]) -> Dict[str, Any]:
        """Generate insurance-specific charts."""
        charts = []
        
        if not scored_neighborhoods:
            return {"charts": []}
        
        # 1. Risk Score Bar Chart (Top 10)
        top_10 = scored_neighborhoods[:10]
        charts.append({
            "type": "bar",
            "title": "Insurance Risk Scores by Neighborhood",
            "data": {
                "labels": [n['neighborhood'] for n in top_10],
                "values": [n['risk_score'] for n in top_10]
            },
            "description": "Computed risk scores (0-100) based on seismic, fire, hazmat, and emergency metrics",
            "color": "danger"
        })
        
        # 2. Risk Tier Distribution (Pie Chart)
        tier_counts = {}
        for n in scored_neighborhoods:
            tier = n['risk_tier']
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        if tier_counts:
            charts.append({
                "type": "pie",
                "title": "Risk Tier Distribution",
                "data": {
                    "labels": list(tier_counts.keys()),
                    "values": list(tier_counts.values())
                },
                "description": "Distribution of neighborhoods across risk tiers (Low/Medium/High/Critical)"
            })
        
        # 3. Risk Drivers Breakdown (Grouped Bar)
        top_5 = scored_neighborhoods[:5]
        charts.append({
            "type": "grouped_bar",
            "title": "Risk Drivers by Top 5 Neighborhoods",
            "data": {
                "labels": [n['neighborhood'] for n in top_5],
                "datasets": [
                    {
                        "label": "Earthquakes",
                        "values": [n['earthquake_events'] for n in top_5],
                        "color": "#8b5cf6"
                    },
                    {
                        "label": "Fires",
                        "values": [n['fire_events'] for n in top_5],
                        "color": "#ef4444"
                    },
                    {
                        "label": "Hazmat",
                        "values": [n['hazmat_events'] for n in top_5],
                        "color": "#f59e0b"
                    }
                ]
            },
            "description": "Breakdown of major risk contributors across high-risk neighborhoods"
        })
        
        # 4. Emergency Load Comparison
        charts.append({
            "type": "grouped_bar",
            "title": "Emergency Call Volume (Top 8 Neighborhoods)",
            "data": {
                "labels": [n['neighborhood'] for n in top_10[:8]],
                "datasets": [
                    {
                        "label": "Police Calls",
                        "values": [n['police_calls'] for n in top_10[:8]],
                        "color": "#3b82f6"
                    },
                    {
                        "label": "EMS Calls",
                        "values": [n['ems_calls'] for n in top_10[:8]],
                        "color": "#10b981"
                    }
                ]
            },
            "description": "Emergency response load indicating operational stress"
        })
        
        return {"charts": charts}
    
    def _generate_chart_data(self, data: List[Dict], chart_suggestions: List[Dict]) -> Dict[str, Any]:
        """Generate chart data for visualization."""
        charts = []
        
        if not data:
            return {"charts": []}
        
        # Get all available columns
        columns = list(data[0].keys()) if data else []
        
        # 1. Bar chart for neighborhood distribution
        if 'neighborhood' in columns:
            neighborhood_data = {}
            for row in data:
                neighborhood = row.get('neighborhood', 'Unknown')
                # Try different count fields
                count = row.get('call_count', row.get('count', row.get('police_calls', row.get('fire_ems_calls', 1))))
                if isinstance(count, (int, float)):
                    neighborhood_data[neighborhood] = neighborhood_data.get(neighborhood, 0) + count
            
            if neighborhood_data:
                # Sort by count and take top 10
                sorted_neighborhoods = sorted(neighborhood_data.items(), key=lambda x: x[1], reverse=True)[:10]
                
                charts.append({
                    "type": "bar",
                    "title": "Top 10 Neighborhoods by Incident Count",
                    "data": {
                        "labels": [item[0] for item in sorted_neighborhoods],
                        "values": [item[1] for item in sorted_neighborhoods]
                    },
                    "description": "Distribution of emergency incidents across San Francisco neighborhoods"
                })
        
        # 2. Pie chart for incident types or call types
        if 'call_type' in columns or 'incident_type' in columns:
            type_field = 'call_type' if 'call_type' in columns else 'incident_type'
            type_counts = {}
            for row in data:
                call_type = row.get(type_field, 'Unknown')
                if call_type and call_type != 'Unknown':
                    type_counts[call_type] = type_counts.get(call_type, 0) + 1
            
            if type_counts:
                # Take top 8 types
                sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:8]
                
                charts.append({
                    "type": "pie",
                    "title": "Emergency Types Distribution",
                    "data": {
                        "labels": [item[0] for item in sorted_types],
                        "values": [item[1] for item in sorted_types]
                    },
                    "description": "Breakdown of emergency incident types"
                })
        
        # 3. Stress score comparison (if available)
        if 'stress_score' in columns and 'neighborhood' in columns:
            stress_data = {}
            for row in data:
                neighborhood = row.get('neighborhood', 'Unknown')
                stress = row.get('stress_score', 0)
                if isinstance(stress, (int, float)) and neighborhood != 'Unknown':
                    stress_data[neighborhood] = stress
            
            if stress_data:
                # Sort by stress score and take top 10
                sorted_stress = sorted(stress_data.items(), key=lambda x: x[1], reverse=True)[:10]
                
                charts.append({
                    "type": "bar",
                    "title": "Neighborhood Stress Scores",
                    "data": {
                        "labels": [item[0] for item in sorted_stress],
                        "values": [round(item[1], 2) for item in sorted_stress]
                    },
                    "description": "Comparative stress levels across neighborhoods",
                    "color": "danger"
                })
        
        # 4. Police vs Fire/EMS comparison (if both available)
        if 'police_calls' in columns and 'fire_ems_calls' in columns and 'neighborhood' in columns:
            comparison_data = {}
            for row in data:
                neighborhood = row.get('neighborhood', 'Unknown')
                police = row.get('police_calls', 0)
                fire_ems = row.get('fire_ems_calls', 0)
                if neighborhood != 'Unknown':
                    comparison_data[neighborhood] = {
                        'police': police,
                        'fire_ems': fire_ems
                    }
            
            if comparison_data:
                # Take top 8 neighborhoods by total calls
                sorted_comparison = sorted(
                    comparison_data.items(), 
                    key=lambda x: x[1]['police'] + x[1]['fire_ems'], 
                    reverse=True
                )[:8]
                
                charts.append({
                    "type": "grouped_bar",
                    "title": "Police vs Fire/EMS Calls by Neighborhood",
                    "data": {
                        "labels": [item[0] for item in sorted_comparison],
                        "datasets": [
                            {
                                "label": "Police Calls",
                                "values": [item[1]['police'] for item in sorted_comparison],
                                "color": "#3b82f6"
                            },
                            {
                                "label": "Fire/EMS Calls",
                                "values": [item[1]['fire_ems'] for item in sorted_comparison],
                                "color": "#ef4444"
                            }
                        ]
                    },
                    "description": "Comparison of police and fire/EMS emergency calls"
                })
        
        # 5. Time series if temporal data exists
        if 'received_datetime' in columns:
            # Extract hour distribution
            hour_counts = {}
            for row in data:
                try:
                    datetime_str = row.get('received_datetime', '')
                    if 'T' in datetime_str:
                        hour = int(datetime_str.split('T')[1].split(':')[0])
                        hour_counts[hour] = hour_counts.get(hour, 0) + 1
                except:
                    continue
            
            if hour_counts:
                # Sort by hour
                sorted_hours = sorted(hour_counts.items())
                charts.append({
                    "type": "line",
                    "title": "Emergency Incidents by Hour of Day",
                    "data": {
                        "labels": [f"{item[0]:02d}:00" for item in sorted_hours],
                        "values": [item[1] for item in sorted_hours]
                    },
                    "description": "Temporal pattern of emergency incidents throughout the day"
                })
        
        # 6. Priority/Severity distribution (if available)
        if 'priority' in columns or 'severity' in columns:
            priority_field = 'priority' if 'priority' in columns else 'severity'
            priority_counts = {}
            for row in data:
                priority = str(row.get(priority_field, 'Unknown'))
                if priority and priority != 'Unknown':
                    priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            if priority_counts:
                sorted_priorities = sorted(priority_counts.items(), key=lambda x: x[1], reverse=True)
                
                charts.append({
                    "type": "pie",
                    "title": "Incident Priority Distribution",
                    "data": {
                        "labels": [item[0] for item in sorted_priorities],
                        "values": [item[1] for item in sorted_priorities]
                    },
                    "description": "Breakdown of incidents by priority level"
                })
        
        return {"charts": charts}
