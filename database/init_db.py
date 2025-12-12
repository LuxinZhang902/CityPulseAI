"""Initialize CityPulse SQLite database with schema."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "citypulse.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

def init_database():
    """Create database and apply schema."""
    print(f"Initializing database at: {DB_PATH}")
    
    # Create database connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read and execute schema
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
    
    cursor.executescript(schema_sql)
    conn.commit()
    
    print("✓ Database schema created successfully")
    
    # Verify tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"✓ Created {len(tables)} tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    conn.close()
    return DB_PATH

if __name__ == "__main__":
    init_database()
