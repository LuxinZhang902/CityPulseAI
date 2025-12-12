"""Real-time data synchronization from SF Open Data APIs."""
import requests
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import time

DB_PATH = Path(__file__).parent.parent.parent / "database" / "citypulse.db"

class RealtimeDataSync:
    """Sync real-time data from SF Open Data portals."""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        
    def sync_police_incidents(self, hours=24):
        """Fetch recent police incidents from SF Open Data."""
        print(f"🚓 Syncing police incidents (last {hours}h)...")
        
        url = "https://data.sfgov.org/resource/wg3w-h783.json"
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        params = {
            "$where": f"incident_datetime > '{cutoff}'",
            "$limit": 1000,
            "$order": "incident_datetime DESC",
            "$select": "incident_number,incident_datetime,incident_category,analysis_neighborhood,latitude,longitude,resolution"
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            count = 0
            for incident in data:
                if not incident.get('incident_number'):
                    continue
                    
                cursor.execute("""
                    INSERT OR REPLACE INTO sf_police_calls_rt 
                    (cad_id, received_datetime, call_type, neighborhood, 
                     latitude, longitude, disposition, priority)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    incident.get('incident_number'),
                    incident.get('incident_datetime'),
                    incident.get('incident_category', 'Unknown'),
                    incident.get('analysis_neighborhood'),
                    float(incident['latitude']) if incident.get('latitude') else None,
                    float(incident['longitude']) if incident.get('longitude') else None,
                    incident.get('resolution', 'Open'),
                    2  # Default priority
                ))
                count += 1
            
            conn.commit()
            conn.close()
            
            print(f"✅ Synced {count} police incidents")
            return count
            
        except Exception as e:
            print(f"❌ Error syncing police data: {e}")
            return 0
    
    def sync_fire_calls(self, hours=24):
        """Fetch recent fire/EMS calls from SF Open Data."""
        print(f"🚒 Syncing fire/EMS calls (last {hours}h)...")
        
        url = "https://data.sfgov.org/resource/nuek-vuh3.json"
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        params = {
            "$where": f"received_dttm > '{cutoff}'",
            "$limit": 1000,
            "$order": "received_dttm DESC"
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            count = 0
            for call in data:
                if not call.get('call_number'):
                    continue
                    
                cursor.execute("""
                    INSERT OR REPLACE INTO sf_fire_ems_calls 
                    (call_number, received_datetime, call_type, neighborhood, 
                     latitude, longitude, disposition)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    call.get('call_number'),
                    call.get('received_dttm'),
                    call.get('call_type', 'Unknown'),
                    call.get('neighborhooods_analysis_boundaries'),
                    float(call['latitude']) if call.get('latitude') else None,
                    float(call['longitude']) if call.get('longitude') else None,
                    call.get('disposition', 'Open')
                ))
                count += 1
            
            conn.commit()
            conn.close()
            
            print(f"✅ Synced {count} fire/EMS calls")
            return count
            
        except Exception as e:
            print(f"❌ Error syncing fire data: {e}")
            return 0
    
    def sync_311_cases(self, days=7):
        """Fetch recent 311 cases from SF Open Data."""
        print(f"📞 Syncing 311 cases (last {days} days)...")
        
        url = "https://data.sfgov.org/resource/vw6y-z8j6.json"
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%S')
        
        params = {
            "$where": f"opened > '{cutoff_date}'",
            "$limit": 500,
            "$order": "opened DESC"
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            count = 0
            for case in data:
                if not case.get('case_id'):
                    continue
                    
                cursor.execute("""
                    INSERT OR REPLACE INTO sf_311_cases 
                    (case_id, opened_datetime, closed_datetime, status, 
                     category, neighborhood, latitude, longitude)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    case.get('case_id'),
                    case.get('opened'),
                    case.get('closed'),
                    case.get('status', 'Open'),
                    case.get('category', 'General'),
                    case.get('neighborhoods_sffind_boundaries'),
                    float(case['lat']) if case.get('lat') else None,
                    float(case['long']) if case.get('long') else None
                ))
                count += 1
            
            conn.commit()
            conn.close()
            
            print(f"✅ Synced {count} 311 cases")
            return count
            
        except Exception as e:
            print(f"❌ Error syncing 311 data: {e}")
            return 0
    
    def sync_earthquakes(self, hours=24):
        """Fetch recent earthquakes near SF from USGS."""
        print(f"🌍 Syncing earthquakes (last {hours}h)...")
        
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = {
            "format": "geojson",
            "starttime": (datetime.now() - timedelta(hours=hours)).isoformat(),
            "latitude": 37.7749,
            "longitude": -122.4194,
            "maxradiuskm": 100,
            "minmagnitude": 1.0
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            count = 0
            for feature in data.get('features', []):
                props = feature['properties']
                coords = feature['geometry']['coordinates']
                
                event_id = f"USGS_{props['ids'].split(',')[0]}"
                
                cursor.execute("""
                    INSERT OR REPLACE INTO sf_disaster_events 
                    (event_id, event_type, description, timestamp, 
                     latitude, longitude, severity, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event_id,
                    'Earthquake',
                    f"Magnitude {props['mag']} earthquake - {props['place']}",
                    datetime.fromtimestamp(props['time']/1000).isoformat(),
                    coords[1],  # latitude
                    coords[0],  # longitude
                    'Critical' if props['mag'] >= 5.0 else 'High' if props['mag'] >= 3.0 else 'Medium',
                    'USGS'
                ))
                count += 1
            
            conn.commit()
            conn.close()
            
            print(f"✅ Synced {count} earthquakes")
            return count
            
        except Exception as e:
            print(f"❌ Error syncing earthquake data: {e}")
            return 0
    
    def sync_all(self):
        """Sync all real-time data sources."""
        print("\n🔄 Starting full data sync...")
        start = time.time()
        
        results = {
            'police': self.sync_police_incidents(hours=24),
            'fire': self.sync_fire_calls(hours=24),
            '311': self.sync_311_cases(days=7),
            'earthquakes': self.sync_earthquakes(hours=24)
        }
        
        elapsed = time.time() - start
        total = sum(results.values())
        
        print(f"\n✅ Sync complete in {elapsed:.1f}s")
        print(f"📊 Total records synced: {total}")
        print(f"   - Police: {results['police']}")
        print(f"   - Fire/EMS: {results['fire']}")
        print(f"   - 311 Cases: {results['311']}")
        print(f"   - Earthquakes: {results['earthquakes']}")
        
        return results


def main():
    """Run a one-time sync."""
    syncer = RealtimeDataSync()
    syncer.sync_all()


if __name__ == "__main__":
    main()
