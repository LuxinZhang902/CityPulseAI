#!/bin/bash

echo "🐾 Setting up SnowLeopard Playground Demo"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Creating template..."
    cat > .env << 'EOF'
# SnowLeopard.ai API Key (REQUIRED)
SNOWLEOPARD_API_KEY=your_snowleopard_api_key_here
EOF
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and add your actual SnowLeopard API key"
    echo ""
fi

# Install playground requirements
echo "📦 Installing SnowLeopard Playground requirements..."
pip install -r playground_requirements.txt

echo ""
echo "🚀 Ready to run Playground demo!"
echo ""
echo "📋 Usage:"
echo "  # Run demo queries"
echo "  python playground_demo.py"
echo ""
echo "  # Interactive mode"
echo "  python playground_demo.py --interactive"
echo ""
echo "📊 Datafile ID: 793f36afcd494309963477d7e7f4075b"
echo "🔑 Make sure your SNOWLEOPARD_API_KEY is set in .env"
