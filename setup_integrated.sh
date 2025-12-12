#!/bin/bash

echo "🐾 Setting up CityPulse AI - Integrated with SnowLeopard Playground"
echo ""

# Check if .env exists and update it
if [ -f ".env" ]; then
    echo "✅ .env file found"
    # Add Playground settings to .env
    if ! grep -q "USE_PLAYGROUND" .env; then
        echo "" >> .env
        echo "# SnowLeopard Playground Settings" >> .env
        echo "USE_PLAYGROUND=true" >> .env
        echo "SNOWLEOPARD_DATAFILE_ID=5baf5ba1d4344af3ba0a56d6869f3352" >> .env
        echo "✅ Added Playground settings to .env"
    fi
else
    echo "❌ .env file not found. Creating with Playground settings..."
    cat > .env << 'EOF'
# SnowLeopard.ai API Key (REQUIRED)
SNOWLEOPARD_API_KEY=your_snowleopard_api_key_here

# SnowLeopard Playground Settings
USE_PLAYGROUND=true
SNOWLEOPARD_DATAFILE_ID=5baf5ba1d4344af3ba0a56d6869f3352

# Google Maps API Key (for frontend)
REACT_APP_GOOGLE_MAPS_API_KEY=AIzaSyD__jUwZNYttgXi5VPcpMW1xHa7_Ea4jEY

# Backend API URL (for frontend)
REACT_APP_API_URL=http://localhost:8000
EOF
fi

# Install integrated requirements
echo "📦 Installing integrated requirements..."
pip install -r backend/requirements_integrated.txt

echo ""
echo "🚀 Integrated setup complete!"
echo ""
echo "📋 Usage:"
echo "  # Start integrated backend"
echo "  python backend/main_integrated.py"
echo ""
echo "  # Test the integration"
echo "  curl -X POST http://localhost:8000/api/analyze \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"question\": \"How many police calls are in the database?\"}'"
echo ""
echo "🔧 New endpoints:"
echo "  GET  /api/status     - Get agent status and mode"
echo "  POST /api/switch-mode - Switch between Playground/Direct API"
echo "  GET  /api/demo-queries - Get demo queries"
echo ""
echo "🎯 Features:"
echo "  ✅ Uses SnowLeopard Playground by default"
echo "  ✅ Falls back to direct API if Playground fails"
echo "  ✅ Shows SQL source in responses"
echo "  ✅ Mode switching at runtime"
