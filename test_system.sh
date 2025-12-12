#!/bin/bash

# CityPulse AI - System Test Script

echo "🧪 CityPulse AI - System Tests"
echo ""

# Test 1: Backend Health
echo "Test 1: Backend Health Check"
response=$(curl -s http://localhost:8000/api/health)
if [ $? -eq 0 ]; then
    echo "✅ Backend is running"
    echo "   Response: $response"
else
    echo "❌ Backend is not responding"
    echo "   Make sure backend is running: cd backend && python main.py"
fi
echo ""

# Test 2: Database Query
echo "Test 2: Sample Query Test"
response=$(curl -s -X POST http://localhost:8000/api/analyze \
    -H "Content-Type: application/json" \
    -d '{"question": "Where is SF under the highest emergency stress right now?"}')
if [ $? -eq 0 ]; then
    echo "✅ Query executed successfully"
    echo "   Analysis type: $(echo $response | grep -o '"analysis_type":"[^"]*"' | cut -d'"' -f4)"
else
    echo "❌ Query failed"
fi
echo ""

# Test 3: Database Check
echo "Test 3: Database Check"
if [ -f "database/citypulse.db" ]; then
    echo "✅ Database file exists"
    
    # Count records
    police_count=$(sqlite3 database/citypulse.db "SELECT COUNT(*) FROM sf_police_calls_rt;")
    fire_count=$(sqlite3 database/citypulse.db "SELECT COUNT(*) FROM sf_fire_ems_calls;")
    
    echo "   Police calls: $police_count"
    echo "   Fire/EMS calls: $fire_count"
else
    echo "❌ Database file not found"
    echo "   Run: python database/init_db.py"
fi
echo ""

# Test 4: Frontend Check
echo "Test 4: Frontend Check"
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend is not responding"
    echo "   Make sure frontend is running: cd frontend && npm start"
fi
echo ""

echo "🎉 System test complete!"
