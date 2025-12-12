#!/usr/bin/env python3
"""
SnowLeopard Playground Demo for CityPulse AI
Uses the official SnowLeopard Playground client to query the uploaded database
"""

from snowleopard import SnowLeopardPlaygroundClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Demo CityPulse AI queries using SnowLeopard Playground"""
    
    # Initialize SnowLeopard Playground client
    api_key = os.getenv("SNOWLEOPARD_API_KEY")
    if not api_key:
        print("❌ Error: SNOWLEOPARD_API_KEY not found in environment")
        print("Please add your API key to .env file")
        return
    
    print("🐾 Initializing SnowLeopard Playground client...")
    client = SnowLeopardPlaygroundClient(api_key=api_key)
    
    # Your uploaded datafile ID
    datafile_id = "b608c4da75b2402a9c4a7a7138ef692f"
    
    print(f"📊 Using datafile_id: {datafile_id}")
    print("=" * 60)
    
    # Demo queries for CityPulse AI
    demo_queries = [
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
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n🔍 Query {i}: {query}")
        print("-" * 50)
        
        try:
            result = client.retrieve(
                datafile_id=datafile_id,
                user_query=query
            )
            
            print("✅ Result:")
            print(result)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("\n" + "=" * 60)
    
    print("\n🎉 Demo completed!")

def interactive_mode():
    """Interactive mode for custom queries"""
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("SNOWLEOPARD_API_KEY")
    
    if not api_key:
        print("❌ Error: SNOWLEOPARD_API_KEY not found")
        return
    
    client = SnowLeopardPlaygroundClient(api_key=api_key)
    datafile_id = "b608c4da75b2402a9c4a7a7138ef692f"
    
    print("🎯 Interactive CityPulse AI Query Mode")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        query = input("\n🔍 Enter your query: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not query:
            continue
        
        try:
            print("\n⏳ Processing...")
            result = client.retrieve(
                datafile_id=datafile_id,
                user_query=query
            )
            print(f"✅ Result:\n{result}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main()
