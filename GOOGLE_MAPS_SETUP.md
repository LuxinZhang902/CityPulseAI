# 🗺️ Google Maps API Setup Guide

## Quick Fix for "InvalidKeyMapError"

You're seeing this error because the Google Maps API key is missing or invalid. Follow these steps:

---

## Option 1: Get a Free Google Maps API Key (Recommended)

### Step 1: Create Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Click **"Select a project"** → **"New Project"**
3. Name it: `CityPulse-AI`
4. Click **"Create"**

### Step 2: Enable Maps JavaScript API

1. In the Google Cloud Console, go to: https://console.cloud.google.com/apis/library
2. Search for: **"Maps JavaScript API"**
3. Click on it
4. Click **"Enable"**

### Step 3: Create API Key

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click **"Create Credentials"** → **"API Key"**
3. Copy the API key (it looks like: `AIzaSyD...`)

### Step 4: Add API Key to Your Project

```bash
cd /Users/luxin/Desktop/Hackathons/In_Person/CityPulseAI_20251212/frontend

# Edit the .env file
nano .env
```

Replace `YOUR_API_KEY_HERE` with your actual API key:

```
REACT_APP_GOOGLE_MAPS_API_KEY=AIzaSyD_your_actual_key_here
REACT_APP_API_URL=http://localhost:8000
```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 5: Restart Frontend

```bash
# Stop the current frontend (Ctrl+C in the terminal running npm start)
# Then restart:
npm start
```

The map should now load! 🎉

---

## Option 2: Use Without Google Maps (Temporary)

If you want to test the system without Google Maps, you can use a simple placeholder map:

### Create a No-Map Version

```bash
cd /Users/luxin/Desktop/Hackathons/In_Person/CityPulseAI_20251212/frontend/src/components
```

I can create a simplified MapView component that shows data in a list format instead of a map.

---

## Option 3: Restrict API Key (After Testing)

Once you have the map working, secure your API key:

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click on your API key
3. Under **"Application restrictions"**:
   - Select **"HTTP referrers"**
   - Add: `http://localhost:3000/*`
4. Under **"API restrictions"**:
   - Select **"Restrict key"**
   - Choose: **"Maps JavaScript API"**
5. Click **"Save"**

---

## Troubleshooting

### Error: "This API project is not authorized to use this API"

- Make sure you **enabled** the Maps JavaScript API in Step 2

### Error: "RefererNotAllowedMapError"

- Your API key has restrictions. Either:
  - Remove restrictions (for testing)
  - Add `http://localhost:3000/*` to allowed referrers

### Map still not loading after adding key

- Make sure you **restarted** the frontend server
- Check the `.env` file has no extra spaces
- Verify the key starts with `AIza`

---

## Free Tier Limits

Google Maps offers:

- **$200 free credit per month**
- For this hackathon project, you'll use approximately:
  - ~1,000 map loads = **$7**
  - Well within free tier! ✅

---

## Current Status

✅ `.env` file created at: `/frontend/.env`  
⚠️ API key is set to: `YOUR_API_KEY_HERE` (placeholder)  
❌ Map will not load until you add a real API key

**Next step:** Follow Option 1 above to get your API key!
