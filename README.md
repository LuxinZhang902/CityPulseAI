# 🌆 CityPulse AI

**Real-Time Urban Crisis Intelligence Agent**  
_Built for the SnowLeopard Hackathon_

CityPulse AI is an advanced multi-signal crisis intelligence agent that uses **SnowLeopard.ai** for natural language to SQL generation, querying live San Francisco emergency data to detect stress patterns, anomalies, and cascading failures.

---

## 🎯 Features

- **Natural Language Queries** → SQL via SnowLeopard.ai
- **Multi-Dataset Joins** (Police, Fire/EMS, 311, Shelter, Disasters)
- **Real-Time Stress Detection** with computed scores
- **AI-Generated Insights** (anomaly detection, correlations, action suggestions)
- **Interactive Crisis Map** (Google Maps with heatmaps + markers)
- **Transparent SQL** (all queries shown in output)

---

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │ ← User asks natural language questions
│  (Google Maps)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Backend│ ← Agent workflow orchestration
│  (Crisis Agent) │
└────────┬────────┘
         │
         ├──► SnowLeopard.ai ← SQL generation
         │
         └──► SQLite DB ← Live crisis data
              (citypulse.db)
```

### Agent Workflow

1. **Interpret Intent** → Classify query type (emergency stress, homelessness, disaster)
2. **Plan Strategy** → Determine tables, metrics, time windows
3. **Generate SQL** → Use SnowLeopard.ai (with fallback)
4. **Execute Query** → Run against live SQLite database
5. **Compute Scores** → Calculate stress/pressure metrics
6. **Generate Insights** → AI-powered anomaly detection
7. **Create Map Layers** → Heatmaps + markers for visualization

---

## 📊 Database Schema

### Tables

| Table                  | Description               | Key Columns                                           |
| ---------------------- | ------------------------- | ----------------------------------------------------- |
| `sf_police_calls_rt`   | 911 police dispatch       | `call_type`, `priority`, `neighborhood`, `lat/lng`    |
| `sf_fire_ems_calls`    | Fire/EMS incidents        | `call_type`, `disposition`, `neighborhood`, `lat/lng` |
| `sf_311_cases`         | Infrastructure complaints | `category`, `status`, `neighborhood`, `lat/lng`       |
| `sf_shelter_waitlist`  | Shelter demand            | `people_waiting`, `shelter_type`, `snapshot_date`     |
| `sf_homeless_baseline` | Unhoused counts           | `unsheltered_count`, `sheltered_count`                |
| `sf_disaster_events`   | Unified disasters         | `event_type`, `severity`, `timestamp`, `lat/lng`      |
| `neighborhoods`        | Metadata                  | `population`, `seniors_65_plus`                       |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- SnowLeopard.ai API key (optional, has fallback)
- Google Maps API key (for frontend)

### 1. Setup Backend

```bash
# Navigate to project root
cd CityPulseAI_20251212

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Initialize database
python database/init_db.py

# Generate sample data
python data/generate_sample_data.py

# Set environment variables
cp .env.example .env
# Edit .env and add your SNOWLEOPARD_API_KEY (optional)

# Start backend server
cd backend
python main.py
```

Backend will run at: `http://localhost:8000`

### 2. Setup Frontend

```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Set environment variables
# Edit .env and add REACT_APP_GOOGLE_MAPS_API_KEY

# Start development server
npm start
```

Frontend will run at: `http://localhost:3000`

---

## 💡 Example Queries

Try these natural language questions:

1. **"Where is SF under the highest emergency stress right now?"**

   - Joins police + fire/EMS data
   - Computes stress score: `police_calls * 1.0 + fire_ems_calls * 1.2`
   - Returns top 10 neighborhoods

2. **"Which neighborhoods show rising homelessness pressure this week?"**

   - Analyzes shelter waitlist trends (7 days)
   - Calculates pressure ratio: `waitlist / capacity`
   - Identifies spikes

3. **"An earthquake hit an hour ago—who is most impacted?"**

   - Filters disaster events (6 hours)
   - Groups by neighborhood + event type
   - Maps severity levels

4. **"Show a map of fire + hazmat incidents in the past 6 hours"**

   - Filters by event type
   - Generates heatmap + markers
   - Color-coded by severity

5. **"Explain why the Tenderloin is a hotspot"**
   - Multi-dataset correlation analysis
   - Identifies contributing factors
   - Suggests interventions

---

## 🔧 API Endpoints

### `POST /api/analyze`

Analyze urban crisis using natural language.

**Request:**

```json
{
  "question": "Where is SF under the highest emergency stress right now?"
}
```

**Response:**

```json
{
  "analysis_type": "emergency_stress",
  "timestamp": "2024-12-11T07:04:00Z",
  "top_neighborhoods": [
    {
      "name": "Tenderloin",
      "metrics": {
        "police_calls": 45,
        "fire_ems_calls": 32,
        "stress_score": 83.4
      }
    }
  ],
  "insight_summary": "🔴 Tenderloin is the highest-stress neighborhood | ⚠️ 47% higher stress than second-ranked | 💡 Deploy additional EMS resources",
  "map_layers": {
    "heatmap": [...],
    "markers": [...],
    "center": {"lat": 37.7749, "lng": -122.4194},
    "zoom": 12
  },
  "sql_used": "SELECT ...",
  "raw_rows": [...]
}
```

### `GET /api/health`

Check backend health and database connectivity.

### `GET /api/schema`

Get database schema information.

---

## 🧪 Testing

### Test Backend

```bash
# Health check
curl http://localhost:8000/api/health

# Test query
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"question": "Where is SF under the highest emergency stress right now?"}'
```

### Test Frontend

1. Open `http://localhost:3000`
2. Click an example query or type your own
3. View results in the sidebar
4. Explore the interactive map

---

## 📁 Project Structure

```
CityPulseAI_20251212/
├── backend/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── crisis_agent.py       # Main agent logic
│   │   └── snowleopard_client.py # SnowLeopard integration
│   ├── main.py                    # FastAPI app
│   └── requirements.txt
├── database/
│   ├── schema.sql                 # Database schema
│   ├── init_db.py                 # Database initializer
│   └── citypulse.db              # SQLite database (generated)
├── data/
│   └── generate_sample_data.py   # Sample data generator
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── QueryPanel.js     # Query input
│   │   │   ├── ResultsPanel.js   # Analysis results
│   │   │   └── MapView.js        # Google Maps integration
│   │   ├── services/
│   │   │   └── api.js            # API client
│   │   ├── App.js                # Main app
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
├── .env.example
├── .gitignore
└── README.md
```

---

## 🎨 Tech Stack

### Backend

- **FastAPI** - High-performance API framework
- **SQLite** - Embedded database
- **SnowLeopard.ai** - Natural language to SQL
- **Python 3.8+**

### Frontend

- **React 18** - UI framework
- **TailwindCSS** - Styling
- **Google Maps API** - Mapping + visualization
- **Lucide React** - Icons
- **Axios** - HTTP client

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```bash
# Optional: SnowLeopard.ai API key
SNOWLEOPARD_API_KEY=your_key_here

# Required: Google Maps API key (for frontend)
REACT_APP_GOOGLE_MAPS_API_KEY=your_key_here

# Backend URL (default: http://localhost:8000)
REACT_APP_API_URL=http://localhost:8000
```

---

## 🚨 Stress Score Formula

```
Emergency Stress Score = (police_calls × 1.0) + (fire_ems_calls × 1.2)
```

Fire/EMS calls weighted higher due to life-threatening nature.

---

## 🤝 Contributing

This is a hackathon project. Feel free to fork and extend!

---

## 📝 License

MIT License - Built for SnowLeopard Hackathon 2024

---

## 🙏 Acknowledgments

- **SnowLeopard.ai** - Natural language SQL generation
- **San Francisco Open Data** - Inspiration for data schema
- **Google Maps Platform** - Mapping infrastructure

---

## 📞 Support

For issues or questions, please open a GitHub issue.

**Built with ❤️ for safer cities**
