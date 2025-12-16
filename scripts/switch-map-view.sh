#!/bin/bash

echo "🗺️  CityPulse AI - Map View Switcher"
echo ""
echo "Choose map version:"
echo "1) Full Google Maps (requires API key)"
echo "2) Simple list view (no API key needed)"
echo ""
read -p "Enter choice (1 or 2): " choice

cd frontend/src/components

if [ "$choice" = "1" ]; then
    if [ -f "MapView.original.js" ]; then
        cp MapView.original.js MapView.js
        echo "✅ Switched to Google Maps version"
        echo "⚠️  Make sure you have a valid API key in frontend/.env"
    else
        echo "✅ Already using Google Maps version"
    fi
elif [ "$choice" = "2" ]; then
    if [ ! -f "MapView.original.js" ]; then
        cp MapView.js MapView.original.js
    fi
    cp MapView.simple.js MapView.js
    echo "✅ Switched to simple list view"
    echo "ℹ️  No API key needed for this version"
else
    echo "❌ Invalid choice"
    exit 1
fi

echo ""
echo "Restart your frontend to see changes:"
echo "  cd frontend && npm start"
