-- Top boroughs by request volume
SELECT borough, request_count, closed_rate_pct, avg_resolution_hours
FROM summary_by_borough
ORDER BY request_count DESC;

-- Top complaint types
SELECT complaint_type, request_count, avg_resolution_hours
FROM summary_by_complaint
ORDER BY request_count DESC
LIMIT 10;

-- Daily request volume
SELECT created_day, request_count
FROM daily_volume
ORDER BY created_day;

-- Priority requests with long resolution times
SELECT unique_key, borough, complaint_type, resolution_hours
FROM service_requests
WHERE priority_flag = TRUE
ORDER BY resolution_hours DESC
LIMIT 10;

-- Open requests by borough
SELECT borough, COUNT(*) AS open_request_count
FROM service_requests
WHERE is_closed = FALSE
GROUP BY borough
ORDER BY open_request_count DESC;
