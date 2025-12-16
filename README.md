# 🌆 CityPulse AI

**Real-Time Urban Crisis Intelligence Platform**

AI-powered emergency response system that analyzes San Francisco's real-time crisis data using natural language queries.

---

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- SnowLeopard AI API key
- Google Maps API key

### Setup

```bash
# Clone & setup
git clone <your-repo-url>
cd CityPulseAI_20251212

# Environment setup
cp .env.example .env
# Edit .env with your API keys
```

### Start Application

```bash
# Sync real-time data (optional)
python scripts/sync_realtime_data.py

# Upload database to SnowLeopard Playground
# File: synced_citypulse_for_playground.db
# Update .env with new datafile ID

# Start backend
cd backend
python main_integrated.py

# Start frontend
cd frontend
npm install
npm start
```

---

## Features

- **AI-Powered Analysis**: Natural language to SQL query generation
- **Real-Time Data**: Live data from SF Open Data APIs
- **Dual-Mode**: City operations + Insurance underwriting
- **Rich Visualizations**: Interactive maps and charts
- **PDF Reports**: Professional report generation

---

## Database Schema

- `sf_police_calls_rt` - Real-time 911 police dispatch calls
- `sf_fire_ems_calls` - Fire department and EMS incidents
- `sf_311_cases` - Non-emergency city service requests
- `sf_shelter_waitlist` - Homeless shelter demand tracking
- `sf_homeless_baseline` - Baseline homeless population counts
- `sf_disaster_events` - Unified disaster events
- `neighborhoods` - SF neighborhood metadata

---

## Architecture

**Backend (FastAPI + Python)**

- `backend/main_integrated.py` - FastAPI server
- `backend/agent/` - Analysis agents and SnowLeopard client
- `backend/services/` - Data sync and PDF generation

**Frontend (React + TailwindCSS)**

- `frontend/src/App.js` - Main app with routing
- `frontend/src/components/` - Maps, queries, results, charts
- `frontend/src/services/` - Backend API client

---

## Scripts

All scripts are located in the `scripts/` directory:

- `sync_realtime_data.py` - Fetch fresh data from SF APIs
- `regenerate_database.sh` - Rebuild database from scratch
- `start.sh` - Start both frontend and backend
- `setup_*.sh` - Various setup scripts

---

## 🎬 Demo Queries

**City Operations Mode**

```
"Where is SF under the highest emergency stress right now?"
"Which neighborhoods have the most fire/EMS calls in the last 24 hours?"
```

**Insurance Underwriting Mode**

```
"Generate an insurance underwriting brief for SoMa after the earthquake.
Include risk tier, top drivers, actions, and show the SQL."
```

---

## Troubleshooting

**Backend won't start**

```bash
pip install -r backend/requirements.txt
cp .env.example .env
```

**No data showing**

```bash
python scripts/sync_realtime_data.py
./scripts/regenerate_database.sh
```

**Frontend won't start**

```bash
cd frontend
npm install
```

---

## Support

For issues or questions:

1. Check troubleshooting section above
2. Verify all environment variables are set
3. Ensure database is uploaded to SnowLeopard
4. Check backend logs for detailed errors

---

**Built with ❤️ for urban crisis intelligence**

_Powered by SnowLeopard AI, FastAPI, React, and San Francisco Open Data_
