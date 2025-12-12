# 🌆 CityPulse AI

**Real-Time Urban Crisis Intelligence Platform**

AI-powered emergency response system that analyzes San Francisco's real-time crisis data using natural language queries. Built with SnowLeopard AI for intelligent SQL generation and comprehensive analysis.

---

## 🎯 Features

### **Dual-Mode Intelligence**

1. **City Operations Mode** - Real-time emergency monitoring and response
2. **Insurance Underwriting Mode** - Risk assessment and portfolio analysis

### **AI-Powered Analysis**

- Natural language to SQL query generation (SnowLeopard AI)
- Two-call architecture: SQL generation + comprehensive AI analysis
- Intelligent fallback system for robust operation
- Risk scoring and tier classification

### **Real-Time Data Integration**

- Live data from SF Open Data APIs
- Police incidents, Fire/EMS calls, 311 cases
- USGS earthquake monitoring
- One-command sync before demos

### **Rich Visualizations**

- Interactive Google Maps with heat layers
- 6 chart types (bar, pie, line, grouped bar, etc.)
- PDF report generation
- Responsive modern UI

---

## 🚀 Quick Start

### **Prerequisites**

- Python 3.8+
- Node.js 16+
- SnowLeopard AI API key ([Get one here](https://snowleopard.ai))
- Google Maps API key ([Get one here](https://console.cloud.google.com/google/maps-apis))

### **1. Clone & Setup**

```bash
git clone <your-repo-url>
cd CityPulseAI_20251212

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys:
# SNOWLEOPARD_API_KEY=your_key_here
# SNOWLEOPARD_DATAFILE_ID=your_datafile_id_here
# REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_key_here
```

### **2. Sync Real-Time Data (Optional but Recommended)**

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Fetch fresh data from SF Open Data APIs
python sync_realtime_data.py

# This syncs:
# - Police incidents (last 24h)
# - Fire/EMS calls (last 24h)
# - USGS earthquakes (last 24h)
```

### **3. Upload Database to SnowLeopard**

```bash
# After syncing, upload to SnowLeopard Playground
# File: synced_citypulse_for_playground.db
# URL: https://playground.snowleopard.ai

# Get the datafile ID and update .env:
# SNOWLEOPARD_DATAFILE_ID=your_new_datafile_id_here
```

### **4. Start Backend**

```bash
cd backend
python main_integrated.py

# Backend runs on: http://localhost:8000
```

### **5. Start Frontend**

```bash
cd frontend
npm install
npm start

# Frontend runs on: http://localhost:3000
```

---

## 📊 Database Schema

### **Tables**

- `sf_police_calls_rt` - Real-time 911 police dispatch calls
- `sf_fire_ems_calls` - Fire department and EMS incidents
- `sf_311_cases` - Non-emergency city service requests
- `sf_shelter_waitlist` - Homeless shelter demand tracking
- `sf_homeless_baseline` - Baseline homeless population counts
- `sf_disaster_events` - Unified disaster events (earthquakes, fires, hazmat)
- `neighborhoods` - SF neighborhood metadata

### **Key Features**

- All tables include `latitude` and `longitude` for mapping
- Timestamps for temporal analysis
- Neighborhood-level aggregation
- Real-time data from SF Open Data APIs

---

## 🎬 Demo Workflow

### **Before Demo**

```bash
# 1. Sync fresh data
python sync_realtime_data.py

# 2. Upload synced_citypulse_for_playground.db to SnowLeopard
# 3. Update .env with new datafile ID
# 4. Start backend and frontend
```

### **Demo Queries**

#### **City Operations Mode**

```
"Where is SF under the highest emergency stress right now?"
"Which neighborhoods have the most fire/EMS calls in the last 24 hours?"
"Show me all hazmat incidents with their severity levels"
```

#### **Insurance Underwriting Mode** (⭐ WOW Moment)

```
"Generate an insurance underwriting brief for SoMa after the earthquake.
Include risk tier, top drivers, actions, and show the SQL."
```

Expected output:

- Risk score (0-100)
- Risk tier (Low/Medium/High/Critical)
- Top risk drivers
- Underwriting recommendations
- Premium adjustment suggestions
- SQL query used

---

## 🏗️ Architecture

### **Backend (FastAPI + Python)**

```
backend/
├── main_integrated.py          # FastAPI server
├── agent/
│   ├── crisis_agent_integrated.py      # Main analysis agent
│   └── snowleopard_client_integrated.py # SnowLeopard API client
└── services/
    ├── realtime_sync.py        # Real-time data sync
    ├── sync_scheduler.py       # Background scheduler
    └── pdf_generator.py        # PDF report generation
```

### **Frontend (React + TailwindCSS)**

```
frontend/src/
├── App.js                      # Main app with routing
├── components/
│   ├── MapView.js             # Google Maps integration
│   ├── QueryPanel.js          # Natural language input
│   ├── ResultsPanel.js        # Analysis results
│   └── ChartsPanel.js         # Visualizations
└── services/
    └── api.js                 # Backend API client
```

### **Data Flow**

```
User Query → Backend API → SnowLeopard AI (2 calls)
                              ↓
                         1. SQL Generation
                         2. AI Analysis
                              ↓
                    Local Execution + Processing
                              ↓
                    Frontend (Maps + Charts)
```

---

## 🔧 Configuration

### **Environment Variables (.env)**

```bash
# SnowLeopard AI
SNOWLEOPARD_API_KEY=your_api_key_here
SNOWLEOPARD_DATAFILE_ID=793f36afcd494309963477d7e7f4075b
USE_PLAYGROUND=true

# Real-time data sync (optional)
SYNC_REALTIME_DATA=false  # Set to 'true' to sync on backend startup

# Google Maps (frontend)
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_key_here
REACT_APP_API_URL=http://localhost:8000
```

### **Backend Configuration**

- Port: 8000
- CORS: Enabled for frontend
- Database: SQLite (`database/citypulse.db`)
- SnowLeopard: Playground mode with datafile ID

### **Frontend Configuration**

- Port: 3000
- Maps: Google Maps JavaScript API
- Charts: Custom React components
- Styling: TailwindCSS + Lucide icons

---

## 📦 Dependencies

### **Backend**

```
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.10.3
requests==2.32.3
python-dotenv==1.0.1
schedule==1.2.0
```

### **Frontend**

```
react
react-dom
@react-google-maps/api
lucide-react
tailwindcss
```

---

## 🎯 Insurance Report Mode

### **Trigger Keywords**

- insurance, underwriting, claims risk, portfolio risk
- exposure, catastrophe report
- insurer, reinsurer, underwriter

### **Risk Scoring Formula**

```
risk_score =
    12 × avg_quake_severity +
    10 × fire_events +
    12 × hazmat_events +
    2 × infra_311_cases +
    0.4 × (ems_calls + police_calls)
```

### **Risk Tiers**

- **0-25**: Low Risk → Normal pricing, annual review
- **26-50**: Medium Risk → 5-10% adjustment, quarterly review
- **51-75**: High Risk → 15-25% increase, quarterly review, 30% inspections
- **76-100**: Critical Risk → Binding pause, 25-40% increase, mandatory inspections

### **Output Fields**

```json
{
  "analysis_type": "insurance_report",
  "risk_summary": "Executive summary...",
  "risk_tier": "High",
  "risk_score": 68.5,
  "top_drivers": ["Fire events: 45", "Hazmat: 12", ...],
  "recommended_actions": ["15-25% rate increase", ...],
  "map_layers": {...},
  "chart_data": {...},
  "sql_used": "SELECT ...",
  "raw_rows": [...]
}
```

---

## 🌐 Real-Time Data Sync

### **Supported APIs**

1. **SF Police Incidents** - https://data.sfgov.org (last 24h)
2. **SF Fire/EMS Calls** - https://data.sfgov.org (last 24h)
3. **SF 311 Cases** - https://data.sfgov.org (last 7 days)
4. **USGS Earthquakes** - https://earthquake.usgs.gov (last 24h, 100km radius)

### **Usage**

```bash
# One-time sync (recommended for demos)
python sync_realtime_data.py

# Or enable automatic sync on backend startup
# Set in .env: SYNC_REALTIME_DATA=true
```

### **What Gets Synced**

- ✅ Real police incidents from last 24 hours
- ✅ Real fire/EMS calls from last 24 hours
- ✅ Real earthquakes from last 24 hours
- ✅ Replaces sample data with live data

---

## 🐛 Troubleshooting

### **Backend won't start**

```bash
# Check Python dependencies
pip install -r backend/requirements.txt

# Verify .env file exists
cp .env.example .env

# Check database exists
ls database/citypulse.db
```

### **Frontend won't start**

```bash
# Install dependencies
cd frontend
npm install

# Clear cache
rm -rf node_modules package-lock.json
npm install
```

### **SnowLeopard errors**

```bash
# Verify API key is set
echo $SNOWLEOPARD_API_KEY

# Check datafile ID is correct
# Upload database to SnowLeopard Playground and get new ID

# System will fallback to local SQL generation if SnowLeopard fails
```

### **No data showing**

```bash
# Regenerate database
./regenerate_database.sh

# Or sync real-time data
python sync_realtime_data.py

# Upload to SnowLeopard and update datafile ID
```

---

## 📈 Performance

### **Response Times**

- SQL Generation: 15-25 seconds (SnowLeopard API)
- AI Analysis: 10-20 seconds (SnowLeopard API)
- Total: 25-45 seconds for complete intelligence
- Fallback: <2 seconds (local SQL generation)

### **Data Sync**

- Police: ~10-15 seconds (up to 1000 records)
- Fire/EMS: ~10-15 seconds (up to 1000 records)
- Earthquakes: ~5 seconds (typically 0-10 events)
- Total: ~30-60 seconds for full sync

---

## 🎨 UI Features

### **Inline Loading State**

- No popup modals
- Beautiful animated loading card
- Non-blocking interface
- Pulsing dots animation

### **Map Visualizations**

- Google Maps integration
- Heat map layers
- Marker clustering
- Neighborhood boundaries

### **Chart Types**

1. Bar Chart - Top neighborhoods by incident count
2. Pie Chart - Emergency types distribution
3. Line Chart - Temporal patterns
4. Grouped Bar Chart - Multi-metric comparison
5. Stress Score Chart - Neighborhood rankings
6. Priority Distribution - Incident priorities

### **PDF Export**

- Click "Download PDF" in results panel
- Includes all analysis, charts, and SQL
- Professional formatting
- Ready for stakeholder distribution

---

## 🔐 Security Notes

- API keys stored in `.env` (gitignored)
- No hardcoded credentials
- CORS configured for localhost only
- Database file gitignored
- Public APIs (no auth required for SF Open Data)

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

This is a hackathon project. For production use:

1. Add authentication/authorization
2. Implement rate limiting
3. Add comprehensive error handling
4. Set up production database (PostgreSQL)
5. Configure production CORS
6. Add monitoring and logging
7. Implement caching layer

---

## 🏆 Hackathon Ready!

### **What Makes This Special**

1. **Dual-Purpose System** - City ops + Insurance underwriting
2. **AI-Powered End-to-End** - Natural language → SQL → Analysis
3. **Real-Time Data** - Live SF emergency data
4. **Production-Grade** - Error handling, fallbacks, PDF export
5. **Beautiful UI** - Modern, responsive, professional

### **Demo Tips**

1. Sync fresh data before demo: `python sync_realtime_data.py`
2. Start with city operations query to show basics
3. WOW moment: Insurance underwriting query
4. Show the SQL that was generated
5. Highlight the AI-powered analysis
6. Export PDF to show stakeholder-ready output

---

## 📞 Support

For issues or questions:

1. Check troubleshooting section above
2. Verify all environment variables are set
3. Ensure database is uploaded to SnowLeopard
4. Check backend logs for detailed errors

---

**Built with ❤️ for urban crisis intelligence**

_Powered by SnowLeopard AI, FastAPI, React, and San Francisco Open Data_
