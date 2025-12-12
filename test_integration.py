#!/usr/bin/env python3
"""Quick test of the integrated CityPulse AI system."""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append('backend')

from agent.crisis_agent_integrated import CityPulseAgent

def test_integration():
    """Test the integrated agent."""
    print("🐾 Testing CityPulse AI - Integrated")
    print("=" * 50)
    
    # Initialize agent
    agent = CityPulseAgent(
        db_path="database/citypulse.db",
        use_playground=True,
        datafile_id="b608c4da75b2402a9c4a7a7138ef692f"
    )
    
    # Show status
    status = agent.get_status()
    print(f"📊 Agent Status:")
    print(f"   SnowLeopard Mode: {status['snowleopard_mode']}")
    print(f"   Database Path: {status['database_path']}")
    print(f"   Tables Count: {status['tables_count']}")
    print(f"   API Key Configured: {status['api_key_configured']}")
    print()
    
    # Test queries
    test_queries = [
        "How many police calls are in the database?",
        "Which neighborhood has the most fire/EMS calls?",
        "What is the total number of 311 cases?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Test Query {i}: {query}")
        print("-" * 40)
        
        try:
            result = agent.analyze(query)
            
            print(f"✅ Analysis Type: {result['analysis_type']}")
            print(f"📝 SQL Source: {result.get('sql_source', 'unknown')}")
            print(f"🔧 SQL Used: {result['sql_used'][:100]}...")
            print(f"💡 Insight: {result['insight_summary'][:100]}...")
            print(f"📊 Raw Rows: {len(result['raw_rows'])}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("\n" + "=" * 50)
    
    print("🎉 Integration test completed!")

if __name__ == "__main__":
    test_integration()
