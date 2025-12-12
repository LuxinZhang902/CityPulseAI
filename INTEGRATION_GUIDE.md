# 🐾 CityPulse AI - SnowLeopard Playground Integration Guide

## 🎯 Overview

Your CityPulse AI system now integrates the SnowLeopard Playground client directly, providing seamless SQL generation with your uploaded database!

---

## ✅ What's Integrated

### 1. **Dual Mode Support**

- **Playground Mode** (default): Uses your uploaded database (`datafile_id: 5baf5ba1d4344af3ba0a56d6869f3352`)
- **Direct API Mode**: Fallback to original SnowLeopard API with schema

### 2. **Smart Fallback System**

- Tries Playground first
- Falls back to Direct API automatically
- Final fallback to rule-based SQL generation

### 3. **Enhanced Responses**

- Shows SQL source (Playground/Direct/Fallback)
- Includes SQL explanation
- Better error handling

---

## 🚀 Quick Setup

### Step 1: Install Integrated Dependencies

```bash
./setup_integrated.sh
```

### Step 2: Verify .env Configuration

```bash
cat .env
```

Should include:

```bash
SNOWLEOPARD_API_KEY=$065f6852141b7cee7e703e75e2dad68877418bb0dcfcb465
USE_PLAYGROUND=true
SNOWLEOPARD_DATAFILE_ID=5baf5ba1d4344af3ba0a56d6869f3352
```

### Step 3: Start Integrated Backend

```bash
python backend/main_integrated.py
```

---

## 🎮 New Features

### 1. **Enhanced API Endpoints**

#### GET /api/status

```json
{
  "snowleopard_mode": "Playground (datafile: 5baf5ba1d4344af3ba0a56d6869f3352)",
  "database_path": "/path/to/citypulse.db",
  "tables_count": 7,
  "api_key_configured": true
}
```

#### POST /api/switch-mode

```bash
curl -X POST http://localhost:8000/api/switch-mode \
  -H "Content-Type: application/json" \
  -d '{"mode": "playground"}'
```

#### GET /api/demo-queries

Returns 10 pre-configured demo queries for testing.

### 2. **Enhanced Query Responses**

Now includes:

```json
{
  "analysis_type": "mixed_query",
  "sql_used": "SELECT COUNT(*) FROM sf_police_calls_rt",
  "sql_source": "playground",
  "sql_explanation": "SQL extracted from Playground response: How many police calls are in the database?",
  "insight_summary": "🔴 Tenderloin is the highest-stress neighborhood",
  "top_neighborhoods": [...],
  "map_layers": {...},
  "raw_rows": [...]
}
```

---

## 🧪 Testing the Integration

### Test 1: Check Status

```bash
curl http://localhost:8000/api/status | python3 -m json.tool
```

### Test 2: Simple Query

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"question": "How many police calls are in the database?"}' \
  | python3 -m json.tool
```

### Test 3: Complex Query

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"question": "Which neighborhoods have the highest emergency stress?"}' \
  | python3 -m json.tool
```

### Test 4: Mode Switching

```bash
# Switch to direct API
curl -X POST http://localhost:8000/api/switch-mode \
  -H "Content-Type: application/json" \
  -d '{"mode": "direct"}'

# Switch back to Playground
curl -X POST http://localhost:8000/api/switch-mode \
  -H "Content-Type: application/json" \
  -d '{"mode": "playground"}'
```

---

## 📁 File Structure

```
CityPulseAI_20251212/
├── backend/
│   ├── agent/
│   │   ├── snowleopard_client_integrated.py    # New: Integrated client
│   │   ├── crisis_agent_integrated.py          # New: Integrated agent
│   │   ├── snowleopard_client.py               # Original: Direct API only
│   │   └── crisis_agent.py                     # Original: Direct API only
│   ├── main_integrated.py                      # New: Integrated FastAPI
│   ├── main.py                                 # Original: Direct API only
│   ├── requirements_integrated.txt              # New: Includes snowleopard
│   └── requirements.txt                        # Original: No snowleopard
├── .env                                        # Updated with Playground settings
├── setup_integrated.sh                         # New: Setup script
└── INTEGRATION_GUIDE.md                        # This file
```

---

## 🔄 Mode Comparison

| Feature         | Playground Mode        | Direct API Mode         |
| --------------- | ---------------------- | ----------------------- |
| **Database**    | Your uploaded datafile | Local schema only       |
| **Setup**       | Just API key needed    | API key + schema        |
| **Performance** | Faster (pre-indexed)   | Slower (schema parsing) |
| **Accuracy**    | Higher (knows data)    | Good (schema-based)     |
| **Fallback**    | ✅ To Direct API       | ✅ To rule-based        |

---

## 🎯 Use Cases

### Use Playground Mode When:

- You want the best SQL accuracy
- You're using the uploaded database
- You need faster query processing
- You're demoing the hackathon project

### Use Direct API Mode When:

- You need schema flexibility
- Playground is unavailable
- You're testing different databases
- You want to compare approaches

---

## 🚨 Troubleshooting

### Issue: "Playground client failed"

**Solution:** System automatically falls back to Direct API

### Issue: "SQL execution failed"

**Solution:** Check the SQL source in response - may need manual adjustment

### Issue: "No data returned"

**Solution:**

1. Check if datafile_id is correct
2. Verify database has data
3. Try switching modes

### Issue: "API key not found"

**Solution:**

1. Check `.env` file
2. Verify `SNOWLEOPARD_API_KEY` is set
3. Restart backend

---

## 🎛️ Configuration Options

In your `.env` file:

```bash
# Required
SNOWLEOPARD_API_KEY=your_actual_key_here

# Playground settings
USE_PLAYGROUND=true                    # true/false
SNOWLEOPARD_DATAFILE_ID=5baf5ba1d4344af3ba0a56d6869f3352

# Frontend (unchanged)
REACT_APP_GOOGLE_MAPS_API_KEY=your_maps_key
REACT_APP_API_URL=http://localhost:8000
```

---

## 🏆 Hackathon Advantages

1. **✅ Uses SnowLeopard Playground** (requirement met)
2. **✅ BYO LLM-API key** (your SnowLeopard key)
3. **✅ SQLite datafile** (uploaded to Playground)
4. **✅ Agent framework** (custom Python + FastAPI)
5. **✅ Working demo** (integrated system)
6. **✅ Fallback resilience** (multiple SQL sources)

---

## 🚀 Next Steps

1. **Run the setup:** `./setup_integrated.sh`
2. **Start integrated backend:** `python backend/main_integrated.py`
3. **Test with demo queries**
4. **Switch between modes to compare**
5. **Ready for 4 PM demo!**

**Your CityPulse AI is now fully integrated with SnowLeopard Playground! 🎉**
