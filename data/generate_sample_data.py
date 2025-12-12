"""Generate realistic sample data for CityPulse AI."""
import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "citypulse.db"

# SF Neighborhoods
NEIGHBORHOODS = [
    "Tenderloin", "SoMa", "Mission", "Bayview", "Chinatown",
    "Financial District", "Nob Hill", "Russian Hill", "Marina",
    "Haight-Ashbury", "Castro", "Potrero Hill", "Dogpatch",
    "Outer Richmond", "Outer Sunset", "Excelsior", "Visitacion Valley"
]

# Coordinates for neighborhoods (approximate centers)
NEIGHBORHOOD_COORDS = {
    "Tenderloin": (37.7849, -122.4194),
    "SoMa": (37.7749, -122.4094),
    "Mission": (37.7599, -122.4148),
    "Bayview": (37.7299, -122.3899),
    "Chinatown": (37.7941, -122.4078),
    "Financial District": (37.7946, -122.3999),
    "Nob Hill": (37.7919, -122.4155),
    "Russian Hill": (37.8011, -122.4189),
    "Marina": (37.8021, -122.4378),
    "Haight-Ashbury": (37.7699, -122.4469),
    "Castro": (37.7609, -122.4350),
    "Potrero Hill": (37.7580, -122.3988),
    "Dogpatch": (37.7599, -122.3888),
    "Outer Richmond": (37.7799, -122.4899),
    "Outer Sunset": (37.7499, -122.4899),
    "Excelsior": (37.7249, -122.4249),
    "Visitacion Valley": (37.7149, -122.4049)
}

POLICE_CALL_TYPES = [
    "Assault", "Burglary", "Robbery", "Theft", "Vandalism",
    "Domestic Violence", "Suspicious Activity", "Traffic Collision",
    "Welfare Check", "Noise Complaint"
]

FIRE_CALL_TYPES = [
    "Medical Emergency", "Structure Fire", "Vehicle Fire", "Alarm",
    "Hazmat", "Gas Leak", "Elevator Rescue", "Water Rescue"
]

CASE_311_CATEGORIES = [
    "Street Cleaning", "Graffiti", "Homeless Encampment", "Abandoned Vehicle",
    "Pothole", "Streetlight Out", "Tree Maintenance", "Illegal Dumping"
]

DISASTER_TYPES = [
    "Fire", "Hazmat", "Earthquake", "Flood", "Power Outage"
]

SEVERITIES = ["Low", "Medium", "High", "Critical"]

def generate_police_calls(conn, count=500):
    """Generate police CAD calls."""
    cursor = conn.cursor()
    now = datetime.now()
    
    for i in range(count):
        neighborhood = random.choice(NEIGHBORHOODS)
        lat, lon = NEIGHBORHOOD_COORDS[neighborhood]
        
        # Add some randomness to coordinates
        lat += random.uniform(-0.01, 0.01)
        lon += random.uniform(-0.01, 0.01)
        
        received = now - timedelta(hours=random.randint(0, 48))
        dispatch = received + timedelta(minutes=random.randint(2, 15))
        closed = dispatch + timedelta(minutes=random.randint(10, 120))
        
        cursor.execute("""
            INSERT INTO sf_police_calls_rt 
            (cad_id, received_datetime, dispatch_datetime, closed_datetime,
             call_type, priority, disposition, neighborhood, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"CAD{i:06d}",
            received.isoformat(),
            dispatch.isoformat(),
            closed.isoformat(),
            random.choice(POLICE_CALL_TYPES),
            random.randint(1, 3),
            random.choice(["Handled", "Report Filed", "Arrest Made", "Unfounded"]),
            neighborhood,
            lat,
            lon
        ))
    
    conn.commit()
    print(f"✓ Generated {count} police calls")

def generate_fire_calls(conn, count=300):
    """Generate fire/EMS calls."""
    cursor = conn.cursor()
    now = datetime.now()
    
    for i in range(count):
        neighborhood = random.choice(NEIGHBORHOODS)
        lat, lon = NEIGHBORHOOD_COORDS[neighborhood]
        
        lat += random.uniform(-0.01, 0.01)
        lon += random.uniform(-0.01, 0.01)
        
        received = now - timedelta(hours=random.randint(0, 48))
        dispatch = received + timedelta(minutes=random.randint(1, 8))
        
        cursor.execute("""
            INSERT INTO sf_fire_ems_calls
            (call_number, incident_number, received_datetime, dispatch_datetime,
             unit_id, call_type, disposition, neighborhood, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"FIRE{i:06d}",
            f"INC{i:06d}",
            received.isoformat(),
            dispatch.isoformat(),
            f"E{random.randint(1, 50)}",
            random.choice(FIRE_CALL_TYPES),
            random.choice(["Transported", "Treated on Scene", "False Alarm", "Cancelled"]),
            neighborhood,
            lat,
            lon
        ))
    
    conn.commit()
    print(f"✓ Generated {count} fire/EMS calls")

def generate_311_cases(conn, count=400):
    """Generate 311 cases."""
    cursor = conn.cursor()
    now = datetime.now()
    
    for i in range(count):
        neighborhood = random.choice(NEIGHBORHOODS)
        lat, lon = NEIGHBORHOOD_COORDS[neighborhood]
        
        lat += random.uniform(-0.01, 0.01)
        lon += random.uniform(-0.01, 0.01)
        
        opened = now - timedelta(days=random.randint(0, 30))
        closed = opened + timedelta(days=random.randint(1, 14)) if random.random() > 0.3 else None
        
        cursor.execute("""
            INSERT INTO sf_311_cases
            (case_id, opened_datetime, closed_datetime, status,
             category, subcategory, neighborhood, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"311-{i:06d}",
            opened.isoformat(),
            closed.isoformat() if closed else None,
            "Closed" if closed else "Open",
            random.choice(CASE_311_CATEGORIES),
            "General",
            neighborhood,
            lat,
            lon
        ))
    
    conn.commit()
    print(f"✓ Generated {count} 311 cases")

def generate_shelter_waitlist(conn):
    """Generate shelter waitlist data."""
    cursor = conn.cursor()
    now = datetime.now()
    
    record_id = 0
    for days_ago in range(7):
        date = now - timedelta(days=days_ago)
        for neighborhood in NEIGHBORHOODS:
            # Tenderloin and SoMa have higher homeless pressure
            base_waiting = 50 if neighborhood in ["Tenderloin", "SoMa"] else 10
            people_waiting = base_waiting + random.randint(-5, 15)
            
            # Get coordinates for neighborhood
            lat, lon = NEIGHBORHOOD_COORDS[neighborhood]
            lat += random.uniform(-0.005, 0.005)
            lon += random.uniform(-0.005, 0.005)
            
            cursor.execute("""
                INSERT INTO sf_shelter_waitlist
                (record_id, snapshot_date, neighborhood, people_waiting, shelter_type, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"SW{record_id:06d}",
                date.date().isoformat(),
                neighborhood,
                people_waiting,
                random.choice(["Emergency", "Transitional", "Navigation Center"]),
                lat,
                lon
            ))
            record_id += 1
    
    conn.commit()
    print(f"✓ Generated shelter waitlist data")

def generate_homeless_baseline(conn):
    """Generate baseline homeless counts."""
    cursor = conn.cursor()
    
    for neighborhood in NEIGHBORHOODS:
        # Tenderloin and SoMa have higher baseline
        if neighborhood in ["Tenderloin", "SoMa"]:
            unsheltered = random.randint(200, 500)
            sheltered = random.randint(150, 300)
        else:
            unsheltered = random.randint(20, 100)
            sheltered = random.randint(10, 50)
        
        # Get coordinates for neighborhood
        lat, lon = NEIGHBORHOOD_COORDS[neighborhood]
        
        cursor.execute("""
            INSERT INTO sf_homeless_baseline
            (neighborhood, unsheltered_count, sheltered_count, snapshot_year, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (neighborhood, unsheltered, sheltered, 2024, lat, lon))
    
    conn.commit()
    print(f"✓ Generated homeless baseline data")

def generate_disaster_events(conn, count=50):
    """Generate disaster events."""
    cursor = conn.cursor()
    now = datetime.now()
    
    for i in range(count):
        neighborhood = random.choice(NEIGHBORHOODS)
        lat, lon = NEIGHBORHOOD_COORDS[neighborhood]
        
        lat += random.uniform(-0.01, 0.01)
        lon += random.uniform(-0.01, 0.01)
        
        timestamp = now - timedelta(hours=random.randint(0, 12))
        event_type = random.choice(DISASTER_TYPES)
        
        cursor.execute("""
            INSERT INTO sf_disaster_events
            (event_id, event_type, description, timestamp,
             latitude, longitude, neighborhood, severity, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"DIS{i:06d}",
            event_type,
            f"{event_type} event in {neighborhood}",
            timestamp.isoformat(),
            lat,
            lon,
            neighborhood,
            random.choice(SEVERITIES),
            random.choice(["SFFD", "USGS", "CalOES", "SF311"])
        ))
    
    conn.commit()
    print(f"✓ Generated {count} disaster events")

def generate_neighborhoods(conn):
    """Generate neighborhood metadata."""
    cursor = conn.cursor()
    
    for neighborhood in NEIGHBORHOODS:
        population = random.randint(10000, 50000)
        seniors = int(population * random.uniform(0.10, 0.20))
        
        cursor.execute("""
            INSERT INTO neighborhoods
            (name, population, seniors_65_plus)
            VALUES (?, ?, ?)
        """, (neighborhood, population, seniors))
    
    conn.commit()
    print(f"✓ Generated neighborhood metadata")

def main():
    """Generate all sample data."""
    print("Generating sample data for CityPulse AI...")
    
    conn = sqlite3.connect(DB_PATH)
    
    # Clear existing data
    cursor = conn.cursor()
    tables = [
        "sf_police_calls_rt", "sf_fire_ems_calls", "sf_311_cases",
        "sf_shelter_waitlist", "sf_homeless_baseline", "sf_disaster_events",
        "neighborhoods"
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
    conn.commit()
    print("✓ Cleared existing data")
    
    # Generate new data
    generate_police_calls(conn, 500)
    generate_fire_calls(conn, 300)
    generate_311_cases(conn, 400)
    generate_shelter_waitlist(conn)
    generate_homeless_baseline(conn)
    generate_disaster_events(conn, 50)
    generate_neighborhoods(conn)
    
    conn.close()
    print("\n✅ Sample data generation complete!")

if __name__ == "__main__":
    main()
