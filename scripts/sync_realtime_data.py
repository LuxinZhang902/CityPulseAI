#!/usr/bin/env python3
"""
One-time sync of real-time data from SF Open Data APIs.
Run this to fetch fresh data before demos or testing.
"""
from backend.services.realtime_sync import RealtimeDataSync

if __name__ == "__main__":
    print("=" * 60)
    print("🌐 CityPulse AI - Real-Time Data Sync")
    print("=" * 60)
    print()
    print("Fetching live data from:")
    print("  • SF Police Incidents (data.sfgov.org)")
    print("  • SF Fire/EMS Calls (data.sfgov.org)")
    print("  • SF 311 Cases (data.sfgov.org)")
    print("  • USGS Earthquakes (earthquake.usgs.gov)")
    print()
    
    syncer = RealtimeDataSync()
    syncer.sync_all()
    
    print()
    print("=" * 60)
    print("✅ Real-time data sync complete!")
    print("=" * 60)
    print()
    print("📋 Next steps:")
    print("  1. Upload database/citypulse.db to SnowLeopard")
    print("  2. Update SNOWLEOPARD_DATAFILE_ID in .env")
    print("  3. Restart backend: python backend/main_integrated.py")
    print()
