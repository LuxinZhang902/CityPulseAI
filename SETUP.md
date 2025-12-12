# 🚀 CityPulse AI - Setup Guide

Complete step-by-step setup instructions.

---

## ⚡ Quick Setup (5 minutes)

### Step 1: Initialize Database

```bash
cd /Users/luxin/Desktop/Hackathons/In_Person/CityPulseAI_20251212

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Initialize database
python database/init_db.py

# Generate sample data (500 police calls, 300 fire/EMS, etc.)
python data/generate_sample_data.py
```

**Expected output:**

```
✓ Database schema created successfully
✓ Created 7 tables
✓ Generated 500 police calls
✓ Generated 300 fire/EMS calls
✓ Generated 400 311 cases
✓ Generated shelter waitlist data
✓ Generated homeless baseline data
✓ Generated 50 disaster events
✓ Generated neighborhood metadata
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env (optional - system works without API keys)
nano .env
```

Add your API keys (optional):

```bash
SNOWLEOPARD_API_KEY=your_snowleopard_key  # Optional - has fallback
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_key  # Required for map
```

### Step 3: Start Backend

```bash
cd backend
python main.py
```

**Expected output:**

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Test backend:

```bash
# In a new terminal
curl http://localhost:8000/api/health
```

### Step 4: Start Frontend

```bash
# In a new terminal
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm start
```

**Expected output:**

```
Compiled successfully!
You can now view citypulse-ai-frontend in the browser.
  Local:            http://localhost:3000
```

---

## 🧪 Verify Installation

### Test 1: Backend Health Check

```bash
curl http://localhost:8000/api/health
```

**Expected response:**

```json
{
  "database": "connected",
  "agent": "ready",
  "snowleopard": "fallback_mode"
}
```

### Test 2: Sample Query

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"question": "Where is SF under the highest emergency stress right now?"}'
```

**Expected response:**

```json
{
  "analysis_type": "emergency_stress",
  "top_neighborhoods": [...],
  "insight_summary": "🔴 Tenderloin is the highest-stress neighborhood...",
  "sql_used": "SELECT ...",
  "raw_rows": [...]
}
```

### Test 3: Frontend

1. Open browser: `http://localhost:3000`
2. Click "Where is SF under the highest emergency stress right now?"
3. Verify results appear in sidebar
4. Verify map shows heatmap + markers

---

## 🔧 Troubleshooting

### Database Issues

**Problem:** `sqlite3.OperationalError: no such table`

**Solution:**

```bash
# Reinitialize database
python database/init_db.py
python data/generate_sample_data.py
```

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**

```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r backend/requirements.txt
```

**Problem:** `Address already in use (port 8000)`

**Solution:**

```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

### Frontend Issues

**Problem:** `Module not found: Can't resolve 'lucide-react'`

**Solution:**

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Problem:** Google Maps not loading

**Solution:**

1. Check `.env` has `REACT_APP_GOOGLE_MAPS_API_KEY`
2. Verify API key has Maps JavaScript API enabled
3. Check browser console for errors

**Problem:** CORS errors

**Solution:**
Backend already has CORS enabled for all origins. If issues persist:

```python
# In backend/main.py, verify:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be present
    ...
)
```

---

## 🎯 Development Workflow

### Making Changes to Backend

```bash
# Backend auto-reloads on file changes
cd backend
uvicorn main:app --reload
```

### Making Changes to Frontend

```bash
# Frontend auto-reloads on file changes
cd frontend
npm start
```

### Regenerating Sample Data

```bash
# Clear and regenerate all data
python data/generate_sample_data.py
```

### Viewing Database

```bash
# Install sqlite3 CLI (if not installed)
brew install sqlite3  # macOS

# Open database
sqlite3 database/citypulse.db

# Run queries
sqlite> SELECT COUNT(*) FROM sf_police_calls_rt;
sqlite> SELECT neighborhood, COUNT(*) FROM sf_fire_ems_calls GROUP BY neighborhood;
sqlite> .quit
```

---

## 📦 Deployment

### Backend Deployment (Production)

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
cd backend
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment (Production)

```bash
cd frontend

# Build production bundle
npm run build

# Serve with static server
npx serve -s build -l 3000
```

### Docker Deployment (Optional)

Create `Dockerfile` in backend:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t citypulse-backend .
docker run -p 8000:8000 citypulse-backend
```

---

## 🔑 API Keys Setup

### SnowLeopard.ai (Optional)

1. Visit: https://snowleopard.ai
2. Sign up for account
3. Generate API key
4. Add to `.env`: `SNOWLEOPARD_API_KEY=your_key`

**Note:** System works without this key using fallback SQL generation.

### Google Maps API (Required for Map)

1. Visit: https://console.cloud.google.com/google/maps-apis
2. Create new project
3. Enable APIs:
   - Maps JavaScript API
   - Places API (optional)
4. Create credentials → API Key
5. Add to `.env`: `REACT_APP_GOOGLE_MAPS_API_KEY=your_key`

**Restrict API key:**

- Application restrictions: HTTP referrers
- Add: `http://localhost:3000/*`
- API restrictions: Maps JavaScript API

---

## 📊 Sample Data Details

Generated data includes:

- **500 police calls** (past 48 hours)

  - Call types: Assault, Burglary, Robbery, Theft, etc.
  - Priorities: 1-3
  - 17 SF neighborhoods

- **300 fire/EMS calls** (past 48 hours)

  - Call types: Medical Emergency, Structure Fire, Hazmat, etc.
  - Unit IDs: E1-E50

- **400 311 cases** (past 30 days)

  - Categories: Graffiti, Homeless Encampment, Potholes, etc.
  - Status: Open/Closed

- **Shelter waitlist** (7 days)

  - Daily snapshots for all neighborhoods
  - Shelter types: Emergency, Transitional, Navigation Center

- **Homeless baseline** (2024)

  - Unsheltered + sheltered counts per neighborhood

- **50 disaster events** (past 12 hours)
  - Types: Fire, Hazmat, Earthquake, Flood, Power Outage
  - Severities: Low, Medium, High, Critical

---

## 🎓 Learning Resources

### Understanding the Agent

Read `backend/agent/crisis_agent.py` to see:

- Intent classification
- SQL strategy planning
- Score computation
- Insight generation

### Understanding SnowLeopard Integration

Read `backend/agent/snowleopard_client.py` to see:

- API integration
- Fallback SQL generation
- Query pattern matching

### Understanding the Frontend

- `src/App.js` - Main application structure
- `src/components/QueryPanel.js` - Natural language input
- `src/components/MapView.js` - Google Maps integration
- `src/components/ResultsPanel.js` - Results visualization

---

## ✅ Next Steps

1. **Customize queries** - Add your own example queries
2. **Extend schema** - Add more data tables
3. **Improve insights** - Enhance AI analysis logic
4. **Add visualizations** - Charts, graphs, timelines
5. **Real-time data** - Connect to live APIs
6. **Mobile app** - React Native version

---

**Need help? Check README.md or open an issue!**
