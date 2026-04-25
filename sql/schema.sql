-- Reference schema for the CityPulse ETL project.
-- The Python loader recreates these tables dynamically from the cleaned DataFrames,
-- but this file documents the intended PostgreSQL warehouse layout.

CREATE TABLE IF NOT EXISTS service_requests (
    unique_key TEXT PRIMARY KEY,
    created_date TIMESTAMP,
    closed_date TIMESTAMP,
    agency TEXT,
    complaint_type TEXT,
    descriptor TEXT,
    borough TEXT,
    status TEXT,
    resolution_hours DOUBLE PRECISION,
    created_day TEXT,
    created_hour BIGINT,
    is_closed BOOLEAN,
    priority_flag BOOLEAN,
    resolution_bucket TEXT
);

CREATE INDEX IF NOT EXISTS idx_requests_borough ON service_requests(borough);
CREATE INDEX IF NOT EXISTS idx_requests_day ON service_requests(created_day);
CREATE INDEX IF NOT EXISTS idx_requests_complaint ON service_requests(complaint_type);
CREATE INDEX IF NOT EXISTS idx_requests_status ON service_requests(status);
