#!/usr/bin/env python3
"""
Quick test for SnowLeopard Playground setup
"""

try:
    from snowleopard import SnowLeopardPlaygroundClient
    print("✅ SnowLeopard Playground client imported successfully")
except ImportError as e:
    print(f"❌ Failed to import SnowLeopard: {e}")
    print("Run: pip install snowleopard")
    exit(1)

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Check API key
api_key = os.getenv("SNOWLEOPARD_API_KEY")
if api_key and api_key != "your_snowleopard_api_key_here":
    print("✅ SnowLeopard API key found")
else:
    print("❌ SnowLeopard API key not set or invalid")
    print("Please edit .env and add your actual API key")
    exit(1)

# Test datafile ID
datafile_id = "5baf5ba1d4344af3ba0a56d6869f3352"
print(f"✅ Datafile ID configured: {datafile_id}")

print("\n🎉 Playground setup test passed!")
print("You can now run: python playground_demo.py")
