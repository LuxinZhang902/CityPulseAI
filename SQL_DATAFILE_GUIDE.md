# 📊 SQL Datafile Guide - CityPulse AI

## 🎯 Your SQL Datafile Location

**Primary:** `database/citypulse.db`  
**Backup:** `citypulse_backup.db` (just created)  
**Size:** 388KB  
**Format:** SQLite 3

---

## 📤 Method 1: Direct File Copy (For Playground Upload)

```bash
# Copy to your Desktop or desired location
cp database/citypulse.db ~/Desktop/citypulse.db

# Or use the backup I just created
cp citypulse_backup.db ~/Desktop/citypulse_for_playground.db
```

**This is the file you upload to SnowLeopard Playground!**

---

## 🔍 Method 2: Explore with SQLite CLI

### Basic Commands

```bash
# Open the database
sqlite3 database/citypulse.db

# Once inside SQLite:
.tables                    # Show all tables
.schema                    # Show table schemas
.schema table_name         # Show specific table schema
.quit                      # Exit SQLite
```

### Example Session

```bash
$ sqlite3 database/citypulse.db
SQLite> .tables
neighborhoods         sf_fire_ems_calls     sf_shelter_waitlist
sf_311_cases          sf_homeless_baseline
sf_disaster_events    sf_police_calls_rt

SQLite> SELECT COUNT(*) FROM sf_police_calls_rt;
500

SQLite> SELECT neighborhood, COUNT(*) FROM sf_police_calls_rt GROUP BY neighborhood LIMIT 5;
Tenderloin|45
SoMa|38
Mission|35
Bayview|32
Chinatown|28

SQLite> .quit
```

---

## 📋 Method 3: Export Data to SQL/CSV

### Export Full Database as SQL

```bash
sqlite3 database/citypulse.db .dump > citypulse_full.sql
```

### Export Specific Table as CSV

```bash
sqlite3 -header -csv database/citypulse.db "SELECT * FROM sf_police_calls_rt LIMIT 10;" > police_sample.csv
```

### Export All Tables as CSV

```bash
# Create a script to export all tables
for table in $(sqlite3 database/citypulse.db ".tables"); do
    sqlite3 -header -csv database/citypulse.db "SELECT * FROM $table;" > ${table}.csv
    echo "Exported $table to ${table}.csv"
done
```

---

## 🌐 Method 4: GUI Tools (Recommended for Exploration)

### Option A: DB Browser for SQLite (Free)

1. Download: https://sqlitebrowser.org/
2. Open: `database/citypulse.db`
3. Browse data, run queries, export

### Option B: DBeaver (Free)

1. Download: https://dbeaver.io/
2. Create new SQLite connection
3. Point to `database/citypulse.db`

### Option C: VS Code Extensions

1. Install "SQLite" extension
2. Open `database/citypulse.db`
3. Query directly in VS Code

---

## 🔧 Method 5: Python Script to Inspect

Create a Python script:

```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('database/citypulse.db')

# Get table info
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
print("Tables:", tables['name'].tolist())

# Sample data from each table
for table in tables['name']:
    print(f"\n--- {table} ---")
    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 3", conn)
    print(df)
    print(f"Total rows: {pd.read_sql(f'SELECT COUNT(*) FROM {table}', conn).iloc[0,0]}")

conn.close()
```

---

## 📊 Quick Data Summary Commands

```bash
# Get row counts for all tables
sqlite3 database/citypulse.db "
SELECT
    name as table_name,
    (SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name = t.name) as exists,
    CASE
        WHEN name = 'sf_police_calls_rt' THEN (SELECT COUNT(*) FROM sf_police_calls_rt)
        WHEN name = 'sf_fire_ems_calls' THEN (SELECT COUNT(*) FROM sf_fire_ems_calls)
        WHEN name = 'sf_311_cases' THEN (SELECT COUNT(*) FROM sf_311_cases)
        WHEN name = 'sf_disaster_events' THEN (SELECT COUNT(*) FROM sf_disaster_events)
        WHEN name = 'neighborhoods' THEN (SELECT COUNT(*) FROM neighborhoods)
        WHEN name = 'sf_shelter_waitlist' THEN (SELECT COUNT(*) FROM sf_shelter_waitlist)
        WHEN name = 'sf_homeless_baseline' THEN (SELECT COUNT(*) FROM sf_homeless_baseline)
    END as row_count
FROM sqlite_master
WHERE type='table'
ORDER BY row_count DESC;
"
```

---

## 🎯 For Hackathon Playground

**Step 1:** Copy the file

```bash
cp database/citypulse.db ./citypulse_for_playground.db
```

**Step 2:** Upload `citypulse_for_playground.db` to SnowLeopard Playground

**Step 3:** Verify it meets requirements:

- ✅ Size: 388KB (under 10MB)
- ✅ Tables: 7 (under 15)
- ✅ Types: Native SQLite (TEXT, INTEGER, REAL)

---

## 🔍 Quick Inspection Commands

```bash
# Check database file info
file database/citypulse.db

# Check database integrity
sqlite3 database/citypulse.db "PRAGMA integrity_check;"

# Get database size
du -h database/citypulse.db

# List all tables with row counts
for table in $(sqlite3 database/citypulse.db ".tables"); do
    count=$(sqlite3 database/citypulse.db "SELECT COUNT(*) FROM $table;")
    echo "$table: $count rows"
done
```

---

## 📁 File Locations Summary

- **Original:** `database/citypulse.db`
- **Backup:** `citypulse_backup.db`
- **For Playground:** `citypulse_for_playground.db` (create this)
- **SQL Export:** `citypulse_full.sql` (create this)
- **CSV Exports:** `table_name.csv` (create these)

**Your SQL datafile is ready! 🚀**
