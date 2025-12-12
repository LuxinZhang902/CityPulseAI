-- CityPulse AI SQLite Schema
-- Real-time urban crisis intelligence database

-- Police CAD calls (real-time 911 dispatch)
CREATE TABLE IF NOT EXISTS sf_police_calls_rt (
    cad_id TEXT PRIMARY KEY,
    received_datetime TEXT NOT NULL,
    dispatch_datetime TEXT,
    closed_datetime TEXT,
    call_type TEXT NOT NULL,
    priority INTEGER,
    disposition TEXT,
    neighborhood TEXT,
    latitude REAL,
    longitude REAL
);

-- Fire/EMS incident data
CREATE TABLE IF NOT EXISTS sf_fire_ems_calls (
    call_number TEXT PRIMARY KEY,
    incident_number TEXT,
    received_datetime TEXT NOT NULL,
    dispatch_datetime TEXT,
    unit_id TEXT,
    call_type TEXT NOT NULL,
    disposition TEXT,
    neighborhood TEXT,
    latitude REAL,
    longitude REAL
);

-- 311 infrastructure/social complaints
CREATE TABLE IF NOT EXISTS sf_311_cases (
    case_id TEXT PRIMARY KEY,
    opened_datetime TEXT NOT NULL,
    closed_datetime TEXT,
    status TEXT,
    category TEXT,
    subcategory TEXT,
    neighborhood TEXT,
    latitude REAL,
    longitude REAL
);

-- Shelter demand tracking
CREATE TABLE IF NOT EXISTS sf_shelter_waitlist (
    record_id TEXT PRIMARY KEY,
    snapshot_date TEXT NOT NULL,
    neighborhood TEXT,
    people_waiting INTEGER,
    shelter_type TEXT
);

-- Baseline unhoused population counts
CREATE TABLE IF NOT EXISTS sf_homeless_baseline (
    neighborhood TEXT PRIMARY KEY,
    unsheltered_count INTEGER,
    sheltered_count INTEGER,
    snapshot_year INTEGER
);

-- Unified disaster events (Fire + Hazmat + Earthquake)
CREATE TABLE IF NOT EXISTS sf_disaster_events (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    description TEXT,
    timestamp TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    neighborhood TEXT,
    severity TEXT,
    source TEXT
);

-- Neighborhood metadata
CREATE TABLE IF NOT EXISTS neighborhoods (
    name TEXT PRIMARY KEY,
    population INTEGER,
    seniors_65_plus INTEGER
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_police_datetime ON sf_police_calls_rt(received_datetime);
CREATE INDEX IF NOT EXISTS idx_police_neighborhood ON sf_police_calls_rt(neighborhood);
CREATE INDEX IF NOT EXISTS idx_fire_datetime ON sf_fire_ems_calls(received_datetime);
CREATE INDEX IF NOT EXISTS idx_fire_neighborhood ON sf_fire_ems_calls(neighborhood);
CREATE INDEX IF NOT EXISTS idx_311_datetime ON sf_311_cases(opened_datetime);
CREATE INDEX IF NOT EXISTS idx_311_neighborhood ON sf_311_cases(neighborhood);
CREATE INDEX IF NOT EXISTS idx_shelter_date ON sf_shelter_waitlist(snapshot_date);
CREATE INDEX IF NOT EXISTS idx_disaster_timestamp ON sf_disaster_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_disaster_neighborhood ON sf_disaster_events(neighborhood);
