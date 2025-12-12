"""Integrated SnowLeopard.ai client for CityPulse AI."""

import time
from typing import Dict, Any, List, Optional
import os
import requests
from snowleopard import SnowLeopardPlaygroundClient

class SnowLeopardClient:
    """
    Integrated SnowLeopard.ai client that supports both:
    1. Direct API calls (original implementation)
    2. Playground client (new integrated approach)
    """
    
    def __init__(self, api_key: Optional[str] = None, use_playground: bool = True, datafile_id: Optional[str] = None):
        self.api_key = api_key or os.getenv("SNOWLEOPARD_API_KEY")
        self.use_playground = use_playground
        self.datafile_id = datafile_id or os.getenv("SNOWLEOPARD_DATAFILE_ID", "b608c4da75b2402a9c4a7a7138ef692f")
        
        # Initialize clients
        if self.use_playground:
            try:
                self.playground_client = SnowLeopardPlaygroundClient(api_key=self.api_key)
                print("✅ SnowLeopard Playground client initialized")
            except Exception as e:
                print(f"⚠️  Playground client failed, falling back to direct API: {e}")
                self.use_playground = False
                self.playground_client = None
        
        # Direct API client (fallback)
        self.base_url = "https://api.snowleopard.ai/v1"
        
    def generate_sql(
        self,
        question: str,
        schema: Dict[str, Any],
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate SQL query using SnowLeopard.ai.
        
        Tries Playground first, falls back to direct API if needed.
        
        Args:
            question: Natural language question
            schema: Database schema information (for direct API only)
            context: Additional context for query generation
            
        Returns:
            Dict with 'sql', 'explanation', and 'confidence'
        """
        try:
            # Try Playground first
            if self.use_playground and self.datafile_id:
                print(f"🐾 Using SnowLeopard Playground: {self.datafile_id}")
                result = self._generate_sql_playground(question, context)
                if result.get("sql"):
                    return result
                print("⚠️  Playground client failed, falling back to direct API")
            
            # Fallback to direct API
            print("🌐 Using SnowLeopard Direct API")
            return self._generate_sql_direct(question, schema, context)
            
        except Exception as e:
            print(f"⚠️  SnowLeopard failed, using fallback: {e}")
            return self._fallback_sql_generation(question, schema)
    
    def _generate_sql_playground(self, question: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Generate SQL using SnowLeopard Playground client."""
        try:
            print("🐾 Starting SnowLeopard Playground SQL generation...")
            print(f"📝 Question: {question}")
            print(f"📁 Datafile ID: {self.datafile_id}")
            
            # Build the full question with enhanced context for location data
            enhanced_context = f"""
            {context or ''}
            
            IMPORTANT SQL GENERATION RULES:
            
            1. LOCATION DATA: Always include latitude and longitude columns in your SELECT statement 
               when querying tables that contain location data. This enables map visualization.
               For SF emergency data tables, always SELECT latitude, longitude along with other columns.
        
            2. AGGREGATION: When asked for counts, totals, or summaries by geographic area 
               (neighborhood, district, etc.), GROUP BY the geographic column ONLY, not by coordinates.
               Use AVG() for latitude and longitude to get center points for map visualization.
               
           EXAMPLE for "calls by neighborhood":
           SELECT 
               neighborhood, 
               COUNT(*) as call_count,
               AVG(latitude) as latitude, 
               AVG(longitude) as longitude
           FROM sf_police_calls_rt 
           WHERE neighborhood IS NOT NULL
           GROUP BY neighborhood
           ORDER BY call_count DESC
        """
            
            full_question = f"{enhanced_context}\n\nQuestion: {question}"
            
            print("🚀 Calling SnowLeopard Playground API...")
            start_time = time.time()
            
            result = self.playground_client.retrieve(
                datafile_id=self.datafile_id,
                user_query=full_question
            )
            print(f"result: {result}")
            
            end_time = time.time()
            print(f"✅ SnowLeopard Playground response received in {end_time - start_time:.2f} seconds")
            print(f"📊 Result type: {type(result)}")
            
            return self._parse_playground_result(result, question)
            
        except Exception as e:
            print(f"⚠️  Playground client failed: {e}")
            return {"sql": "", "explanation": f"Playground error: {str(e)}", "confidence": 0.0}
    
    def _generate_sql_direct(
        self,
        question: str,
        schema: Dict[str, Any],
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate SQL using direct SnowLeopard API (original implementation)."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Enhanced context to include location requirements
        enhanced_context = f"""
        {context or ''}
        
        IMPORTANT SQL GENERATION RULES:
        
        1. LOCATION DATA: Always include latitude and longitude columns in your SELECT statement 
           when querying tables that contain location data. This enables map visualization.
           For SF emergency data tables, always SELECT latitude, longitude along with other columns.
        
        2. AGGREGATION: When asked for counts, totals, or summaries by geographic area 
           (neighborhood, district, etc.), GROUP BY the geographic column ONLY, not by coordinates.
           Use AVG() for latitude and longitude to get center points for map visualization.
           
           EXAMPLE for "calls by neighborhood":
           SELECT 
               neighborhood, 
               COUNT(*) as call_count,
               AVG(latitude) as latitude, 
               AVG(longitude) as longitude
           FROM sf_police_calls_rt 
           WHERE neighborhood IS NOT NULL 
           GROUP BY neighborhood 
           ORDER BY call_count DESC
        
        3. MAP VISUALIZATION: For geographic queries, always include:
           - The grouping column (neighborhood, district, etc.)
           - The count/aggregate metric 
           - AVG(latitude) as latitude for map center
           - AVG(longitude) as longitude for map center
        """
        
        payload = {
            "question": question,
            "schema": schema,
            "dialect": "sqlite",
            "context": enhanced_context
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
            print(f"⚠️  Direct API failed, using fallback: {e}")
            return self._fallback_sql_generation(question, schema)
    
    def _parse_playground_result(self, result, original_question: str) -> Dict[str, Any]:
        """Parse Playground result to extract SQL, data, and complete solution."""
        try:
            print("🔍 Parsing SnowLeopard Playground result...")
            
            # Extract data from RetrieveResponse
            if hasattr(result, 'data') and result.data:
                print(f"📋 Found {len(result.data)} data items in result")
                data_item = result.data[0]
                
                # Check if this is an ErrorSchemaData (SnowLeopard returned a SQL error)
                class_name = data_item.__class__.__name__
                if 'Error' in class_name or hasattr(data_item, 'error'):
                    error_msg = getattr(data_item, 'error', getattr(data_item, 'message', 'Unknown error from SnowLeopard'))
                    print(f"⚠️  SnowLeopard returned SQL error: {error_msg[:200]}...")
                    print(f"🔄 Falling back to local SQL generation")
                    return self._fallback_sql_generation(original_question, {})
                
                # Check if data_item has the required attributes for successful response
                if not hasattr(data_item, 'query'):
                    print(f"⚠️  Invalid data item structure (no query): {type(data_item)}")
                    return self._fallback_sql_generation(original_question, {})
                
                if not hasattr(data_item, 'rows'):
                    print(f"⚠️  Invalid data item structure (no rows): {type(data_item)}")
                    return self._fallback_sql_generation(original_question, {})
                
                sql = data_item.query
                rows = data_item.rows if data_item.rows else []
                
                print(f"📊 Extracted SQL: {sql[:100]}..." if len(sql) > 100 else f"📊 Extracted SQL: {sql}")
                print(f"📈 Extracted {len(rows)} rows of data")
                
                # Extract query summary (handle both dict and object formats)
                query_summary = data_item.querySummary
                if isinstance(query_summary, dict):
                    explanation = query_summary.get('non_technical_explanation', f"Generated by SnowLeopard Playground for: {original_question}")
                    technical_details = query_summary.get('technical_details', '')
                else:
                    explanation = getattr(query_summary, 'non_technical_explanation', f"Generated by SnowLeopard Playground for: {original_question}")
                    technical_details = getattr(query_summary, 'technical_details', '')
                
                confidence = 0.9  # High confidence for Playground
                
                # SECOND SNOWLEOPARD CALL: Generate comprehensive analysis/summary
                print("🧠 Calling SnowLeopard for comprehensive analysis...")
                analysis_start = time.time()
                analysis_result = self._generate_snowleopard_analysis(original_question, rows, sql, explanation)
                analysis_end = time.time()
                print(f"✅ Analysis completed in {analysis_end - analysis_start:.2f} seconds")
                
                print("🎯 SnowLeopard Playground processing complete!")
                return {
                    'sql': sql,
                    'explanation': explanation,
                    'technical_details': technical_details,
                    'confidence': confidence,
                    'rows': rows,
                    'snowleopard_solution': True,
                    'analysis': analysis_result
                }
            else:
                print("⚠️  No data in Playground result")
                return self._fallback_sql_generation(original_question, {})
                
        except Exception as e:
            print(f"⚠️  Error parsing Playground result: {e}")
            return self._fallback_sql_generation(original_question, {})
    
    def _generate_snowleopard_analysis(self, question: str, data: List[Dict], sql: str, sql_explanation: str) -> Dict[str, Any]:
        """
        SECOND SNOWLEOPARD CALL: Generate comprehensive analysis using SnowLeopard Playground.
        This provides AI-powered insights, risk assessment, and recommendations.
        """
        try:
            # Prepare data summary for analysis
            data_summary = {
                'row_count': len(data),
                'columns': list(data[0].keys()) if data else [],
                'sample_rows': data[:5] if len(data) > 5 else data,
                'top_values': {}
            }
            
            # Extract key metrics from data
            if data:
                for key in data[0].keys():
                    if key in ['neighborhood', 'event_type', 'call_type']:
                        # Get top categorical values
                        values = [row.get(key) for row in data[:10] if row.get(key)]
                        data_summary['top_values'][key] = list(set(values))[:5]
            
            # Build analysis prompt for SnowLeopard
            analysis_prompt = f"""
Based on the following emergency data analysis, provide a comprehensive urban crisis intelligence report:

ORIGINAL QUESTION: {question}

SQL QUERY EXECUTED: {sql}

SQL EXPLANATION: {sql_explanation}

DATA SUMMARY:
- Total Records: {data_summary['row_count']}
- Columns: {', '.join(data_summary['columns'])}
- Sample Data: {data_summary['sample_rows']}

Please provide a comprehensive analysis in JSON format with these exact keys:
{{
    "executive_summary": "2-3 sentence high-level summary of findings for city officials or insurance underwriters",
    "key_insights": ["insight 1", "insight 2", "insight 3"],
    "trend_analysis": "What patterns or trends emerge from this data",
    "risk_assessment": {{
        "level": "LOW|MEDIUM|HIGH|CRITICAL",
        "reasoning": "Why this risk level was assigned"
    }},
    "recommendations": ["actionable recommendation 1", "actionable recommendation 2", "actionable recommendation 3"],
    "chart_suggestions": [
        {{
            "type": "bar|pie|line",
            "title": "Chart title",
            "description": "What this chart shows"
        }}
    ]
}}

Focus on actionable insights for emergency response, resource allocation, or insurance underwriting.
"""
            
            # Call SnowLeopard Playground for analysis
            print(f"📤 Sending analysis request to SnowLeopard (data: {len(data)} rows)...")
            
            result = self.playground_client.retrieve(
                datafile_id=self.datafile_id,
                user_query=analysis_prompt
            )
            
            # Parse the analysis response
            if hasattr(result, 'data') and result.data:
                data_item = result.data[0]
                
                # Try to extract structured analysis from the response
                if hasattr(data_item, 'querySummary'):
                    query_summary = data_item.querySummary
                    
                    # Try to parse as JSON if it's a string
                    if isinstance(query_summary, str):
                        import json
                        try:
                            analysis_json = json.loads(query_summary)
                            print("✅ Successfully parsed SnowLeopard analysis as JSON")
                            return analysis_json
                        except:
                            pass
                    
                    # Try to extract from dict/object
                    if isinstance(query_summary, dict):
                        return {
                            "executive_summary": query_summary.get('non_technical_explanation', sql_explanation),
                            "key_insights": [query_summary.get('technical_details', 'Analysis completed')],
                            "trend_analysis": query_summary.get('non_technical_explanation', ''),
                            "risk_assessment": {
                                "level": "MEDIUM",
                                "reasoning": "Based on SnowLeopard analysis"
                            },
                            "recommendations": ["Monitor trends", "Allocate resources based on findings"],
                            "chart_suggestions": []
                        }
            
            # Fallback to local analysis if SnowLeopard analysis fails
            print("⚠️  SnowLeopard analysis parsing failed, using local analysis")
            return self._create_analysis_from_data(question, data, sql, sql_explanation, "")
            
        except Exception as e:
            print(f"⚠️  SnowLeopard analysis failed: {e}, using local analysis")
            return self._create_analysis_from_data(question, data, sql, sql_explanation, "")
    
    def _create_analysis_from_data(self, question: str, data: List[Dict], sql: str, 
                                       explanation: str, technical_details: str) -> Dict[str, Any]:
        """Create comprehensive analysis from retrieved data without additional API calls."""
        try:
            row_count = len(data)
            
            # Extract insights from the data
            insights = []
            neighborhoods = []
            risk_level = "MEDIUM"
            
            if row_count > 0 and data:
                # Analyze data structure
                columns = list(data[0].keys())
                
                # Extract neighborhood information
                if 'neighborhood' in columns:
                    neighborhoods = [row.get('neighborhood') for row in data if row.get('neighborhood')]
                    unique_neighborhoods = len(set(neighborhoods))
                    insights.append(f"Analysis covers {unique_neighborhoods} neighborhoods across San Francisco")
                
                # Analyze metrics
                if 'stress_score' in columns or 'count' in columns or 'call_count' in columns:
                    insights.append(f"Analyzed {row_count} data points showing emergency patterns")
                    
                    # Determine risk level based on data volume
                    if row_count > 50:
                        risk_level = "HIGH"
                        insights.append("High volume of incidents indicates elevated urban stress")
                    elif row_count > 20:
                        risk_level = "MEDIUM"
                        insights.append("Moderate incident levels require continued monitoring")
                    else:
                        risk_level = "LOW"
                
                # Add spatial insight
                if 'latitude' in columns and 'longitude' in columns:
                    insights.append("Geographic coordinates enable precise spatial analysis and mapping")
            
            # Build executive summary from explanation
            executive_summary = explanation if explanation else f"Analysis of {row_count} records provides insights into urban emergency patterns."
            
            # Generate recommendations based on question type
            recommendations = []
            question_lower = question.lower()
            if 'homeless' in question_lower or 'shelter' in question_lower:
                recommendations = [
                    "Increase shelter capacity in high-impact neighborhoods",
                    "Deploy mobile outreach teams to identified hotspots",
                    "Coordinate with social services for comprehensive support"
                ]
            elif 'emergency' in question_lower or 'stress' in question_lower:
                recommendations = [
                    "Enhance emergency response resources in high-stress areas",
                    "Implement predictive monitoring for early intervention",
                    "Coordinate multi-agency response protocols"
                ]
            else:
                recommendations = [
                    "Monitor trends for early warning signs",
                    "Allocate resources based on geographic patterns",
                    "Implement data-driven intervention strategies"
                ]
            
            # Suggest chart types based on data structure
            chart_suggestions = []
            if data and len(data) > 0:
                if 'neighborhood' in data[0]:
                    chart_suggestions.append({
                        "type": "bar",
                        "title": "Incidents by Neighborhood",
                        "description": "Compare incident counts across neighborhoods"
                    })
                if 'latitude' in data[0] and 'longitude' in data[0]:
                    chart_suggestions.append({
                        "type": "heatmap",
                        "title": "Geographic Distribution",
                        "description": "Visualize incident density across the city"
                    })
            
            return {
                "executive_summary": executive_summary,
                "key_insights": insights if insights else ["Data analysis completed successfully"],
                "trend_analysis": technical_details if technical_details else "Spatial and temporal patterns analyzed for urban crisis management.",
                "risk_assessment": {
                    "level": risk_level,
                    "reasoning": f"Based on analysis of {row_count} records and observed patterns."
                },
                "recommendations": recommendations,
                "chart_suggestions": chart_suggestions
            }
            
        except Exception as e:
            print(f"⚠️  Error creating analysis from data: {e}")
            return self._create_fallback_analysis(question, data)
    
    def _create_fallback_analysis(self, question: str, data: List[Dict]) -> Dict[str, Any]:
        """Create fallback analysis when SnowLeopard analysis fails."""
        row_count = len(data)
        
        # Basic insights based on data
        insights = []
        if row_count > 0:
            insights.append(f"Analysis of {row_count} records provides comprehensive coverage")
            if 'neighborhood' in data[0]:
                neighborhoods = set(row.get('neighborhood') for row in data if row.get('neighborhood'))
                insights.append(f"Data spans {len(neighborhoods)} different neighborhoods")
        
        return {
            "executive_summary": f"Analysis of {row_count} emergency records reveals key patterns for urban crisis management.",
            "key_insights": insights or ["Data analysis completed successfully"],
            "trend_analysis": "Spatial distribution shows varied emergency patterns across neighborhoods.",
            "risk_assessment": {
                "level": "MEDIUM",
                "reasoning": "Based on current data patterns and distribution."
            },
            "recommendations": [
                "Monitor high-frequency areas for resource allocation",
                "Consider temporal patterns for emergency response planning"
            ],
            "chart_suggestions": [
                {
                    "type": "bar",
                    "title": "Emergency Distribution by Neighborhood",
                    "description": "Shows volume of incidents across different areas"
                }
            ]
        }
    
    def _fallback_sql_generation(
        self,
        question: str,
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback SQL generation when both Playground and direct API fail.
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
            HAVING neighborhood IS NOT NULL
            ORDER BY stress_score DESC
            LIMIT 20
            """
            return {
            "sql": sql,
            "explanation": "Emergency stress analysis for past 24 hours combining police and fire/EMS calls",
            "confidence": 0.85,
            "source": "fallback",
            "has_solution": False
        }
        
        # Insurance/underwriting queries
        if any(kw in question_lower for kw in ["insurance", "underwriting", "risk", "exposure"]):
            sql = """
            SELECT 
                p.neighborhood,
                COUNT(DISTINCT p.cad_id) as police_calls,
                COUNT(DISTINCT f.call_number) as ems_calls,
                0 as earthquake_events,
                0 as avg_quake_severity,
                0 as fire_events,
                0 as hazmat_events,
                0 as infra_311_cases,
                AVG(p.latitude) as latitude,
                AVG(p.longitude) as longitude
            FROM sf_police_calls_rt p
            LEFT JOIN sf_fire_ems_calls f ON p.neighborhood = f.neighborhood
            WHERE p.neighborhood IS NOT NULL
                AND datetime(p.received_datetime) >= datetime('now', '-7 days')
            GROUP BY p.neighborhood
            ORDER BY police_calls DESC
            LIMIT 20
            """
            return {
                "sql": sql,
                "explanation": "Insurance risk assessment query (fallback - limited disaster data)",
                "confidence": 0.75,
                "source": "fallback",
                "has_solution": False
            }
        
        # Police calls by neighborhood
        if "police" in question_lower and "neighborhood" in question_lower:
            sql = """
            SELECT 
                neighborhood,
                COUNT(*) as call_count,
                AVG(latitude) as latitude,
                AVG(longitude) as longitude
            FROM sf_police_calls_rt
            WHERE neighborhood IS NOT NULL
                AND datetime(received_datetime) >= datetime('now', '-24 hours')
            GROUP BY neighborhood
            ORDER BY call_count DESC
            LIMIT 20
            """
            return {
                "sql": sql,
                "explanation": "Police calls by neighborhood for past 24 hours",
                "confidence": 0.85,
                "source": "fallback",
                "has_solution": False
            }
        
        # Homeless/shelter queries
        if "homeless" in question_lower or "shelter" in question_lower:
            sql = """
            SELECT 
                neighborhood,
                COUNT(*) as incidents,
                AVG(latitude) as latitude,
                AVG(longitude) as longitude
            FROM sf_311_cases
            WHERE neighborhood IS NOT NULL
                AND datetime(created_date) >= datetime('now', '-7 days')
            GROUP BY neighborhood
            ORDER BY incidents DESC
            LIMIT 20
            """
            return {
                "sql": sql,
                "explanation": "311 cases analysis for homelessness indicators",
                "confidence": 0.75,
                "source": "fallback",
                "has_solution": False
            }
        
        # Disaster/earthquake queries
        if "disaster" in question_lower or "earthquake" in question_lower:
            sql = """
            SELECT 
                neighborhood,
                COUNT(*) as event_count,
                AVG(severity) as avg_severity,
                AVG(latitude) as latitude,
                AVG(longitude) as longitude
            FROM sf_disaster_events
            WHERE neighborhood IS NOT NULL
                AND datetime(event_datetime) >= datetime('now', '-7 days')
            GROUP BY neighborhood
            ORDER BY event_count DESC
            LIMIT 20
            """
            return {
                "sql": sql,
                "explanation": "Disaster events analysis for past 7 days",
                "confidence": 0.85,
                "source": "fallback",
                "has_solution": False
            }
        
        # Simple count queries
        if "how many" in question_lower:
            if "police" in question_lower:
                sql = "SELECT COUNT(*) as police_calls FROM sf_police_calls_rt WHERE datetime(received_datetime) >= datetime('now', '-24 hours')"
            elif "fire" in question_lower or "ems" in question_lower:
                sql = "SELECT COUNT(*) as fire_ems_calls FROM sf_fire_ems_calls WHERE datetime(received_datetime) >= datetime('now', '-24 hours')"
            elif "311" in question_lower:
                sql = "SELECT COUNT(*) as cases_311 FROM sf_311_cases WHERE datetime(created_date) >= datetime('now', '-7 days')"
            elif "disaster" in question_lower:
                sql = "SELECT COUNT(*) as disaster_events FROM sf_disaster_events WHERE datetime(event_datetime) >= datetime('now', '-7 days')"
            else:
                sql = """
                SELECT 
                    'police' as category, COUNT(*) as count FROM sf_police_calls_rt WHERE datetime(received_datetime) >= datetime('now', '-24 hours')
                UNION ALL
                SELECT 
                    'fire_ems' as category, COUNT(*) as count FROM sf_fire_ems_calls WHERE datetime(received_datetime) >= datetime('now', '-24 hours')
                """
            
            return {
                "sql": sql,
                "explanation": "Count query for recent emergency data",
                "confidence": 0.80,
                "source": "fallback",
                "has_solution": False
            }
        
        # Generic neighborhood query
        if "neighborhood" in question_lower:
            sql = """
            SELECT 
                p.neighborhood,
                COUNT(DISTINCT p.cad_id) as police_calls,
                COUNT(DISTINCT f.call_number) as fire_ems_calls,
                AVG(p.latitude) as latitude,
                AVG(p.longitude) as longitude
            FROM sf_police_calls_rt p
            LEFT JOIN sf_fire_ems_calls f ON p.neighborhood = f.neighborhood
            WHERE p.neighborhood IS NOT NULL
                AND datetime(p.received_datetime) >= datetime('now', '-24 hours')
            GROUP BY p.neighborhood
            ORDER BY police_calls DESC
            LIMIT 20
            """
            return {
                "sql": sql,
                "explanation": "Emergency calls by neighborhood for past 24 hours",
                "confidence": 0.80,
                "source": "fallback",
                "has_solution": False
            }
        
        # Default fallback - return recent emergency summary
        sql = """
        SELECT 
            p.neighborhood,
            COUNT(DISTINCT p.cad_id) as police_calls,
            COUNT(DISTINCT f.call_number) as fire_ems_calls,
            AVG(p.latitude) as latitude,
            AVG(p.longitude) as longitude
        FROM sf_police_calls_rt p
        LEFT JOIN sf_fire_ems_calls f ON p.neighborhood = f.neighborhood
        WHERE p.neighborhood IS NOT NULL
            AND datetime(p.received_datetime) >= datetime('now', '-24 hours')
        GROUP BY p.neighborhood
        ORDER BY police_calls DESC
        LIMIT 20
        """
        return {
            "sql": sql,
            "explanation": "General emergency overview by neighborhood (default fallback)",
            "confidence": 0.70,
            "source": "fallback",
            "has_solution": False
        }
    
    def switch_to_playground(self, datafile_id: Optional[str] = None):
        """Switch to Playground mode."""
        if datafile_id:
            self.datafile_id = datafile_id
        
        try:
            self.playground_client = SnowLeopardPlaygroundClient(api_key=self.api_key)
            self.use_playground = True
            print(f"✅ Switched to Playground mode with datafile: {self.datafile_id}")
        except Exception as e:
            print(f"❌ Failed to switch to Playground: {e}")
            self.use_playground = False
    
    def switch_to_direct_api(self):
        """Switch to direct API mode."""
        self.use_playground = False
        print("✅ Switched to direct API mode")
    
    def get_mode(self) -> str:
        """Get current mode."""
        if self.use_playground:
            return f"Playground (datafile: {self.datafile_id})"
        else:
            return "Direct API"
