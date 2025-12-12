#!/bin/bash

# CityPulse AI - Quick Start Script

echo "🌆 CityPulse AI - Starting System..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
if [ ! -f "venv/.installed" ]; then
    echo "📥 Installing backend dependencies..."
    pip install -r backend/requirements.txt > /dev/null 2>&1
    touch venv/.installed
    echo "✅ Backend dependencies installed"
fi

# Initialize database if it doesn't exist
if [ ! -f "database/citypulse.db" ]; then
    echo "🗄️  Initializing database..."
    python database/init_db.py
    
    echo "📊 Generating sample data..."
    python data/generate_sample_data.py
    echo "✅ Database ready"
else
    echo "✅ Database already exists"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your API keys"
fi

# Start backend
echo ""
echo "🚀 Starting backend server on http://localhost:8000..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📥 Installing frontend dependencies..."
    cd frontend
    npm install > /dev/null 2>&1
    cd ..
    echo "✅ Frontend dependencies installed"
fi

# Start frontend
echo "🚀 Starting frontend on http://localhost:3000..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ CityPulse AI is running!"
echo ""
echo "📍 Backend:  http://localhost:8000"
echo "📍 Frontend: http://localhost:3000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C to kill both processes
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Wait for processes
wait
