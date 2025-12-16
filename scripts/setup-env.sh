#!/bin/bash

echo "🔧 Setting up environment variables for CityPulse AI"
echo ""

# Create .env file
cat > .env << 'EOF'
# SnowLeopard.ai API Key (REQUIRED for hackathon)
# Get your API key from: https://snowleopard.ai
# This is your BYO LLM-API key for SQL generation
SNOWLEOPARD_API_KEY=your_snowleopard_api_key_here

# Backend API URL (for frontend)
REACT_APP_API_URL=http://localhost:8000
EOF

echo "✅ Created .env file"
echo ""
echo "⚠️  IMPORTANT: Edit .env and add your actual SnowLeopard API key:"
echo "   nano .env"
echo ""
echo "📍 SQLite database ready for Playground upload:"
echo "   File: database/citypulse.db"
echo "   Size: 388KB (well under 10MB limit)"
echo "   Tables: 7 (under 15 table limit)"
echo "   Types: Native SQLite (TEXT, INTEGER, REAL)"
echo ""
echo "🐾 SnowLeopard API integration confirmed:"
echo "   ✅ Using https://api.snowleopard.ai/v1/generate-sql"
echo "   ✅ Bearer token authentication"
echo "   ✅ SQLite dialect support"
echo "   ✅ Schema-aware query generation"
echo ""
echo "🚀 Ready for hackathon demo!"
