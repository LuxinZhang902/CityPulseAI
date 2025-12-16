#!/bin/bash
# Regenerate CityPulse database with updated schema

echo "🗑️  Removing old database..."
rm -f database/citypulse.db

echo "🏗️  Creating new database with updated schema..."
python database/init_db.py

echo "📊 Generating sample data with lat/lon for all tables..."
python data/generate_sample_data.py

echo "✅ Database regenerated successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Upload the new database/citypulse.db to SnowLeopard"
echo "2. Get the new datafile ID"
echo "3. Update SNOWLEOPARD_DATAFILE_ID in .env"
echo "4. Restart the backend: python backend/main_integrated.py"
