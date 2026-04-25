# Data Dictionary

## Cleaned service request fields

| Column | Description |
|---|---|
| `unique_key` | Original unique service request identifier from the raw file |
| `created_date` | Timestamp when the request was opened |
| `closed_date` | Timestamp when the request was closed, if available |
| `agency` | Responsible agency code |
| `complaint_type` | Standardized complaint category |
| `descriptor` | More specific issue description |
| `borough` | Normalized borough value |
| `status` | Normalized request status |
| `incident_zip` | ZIP code associated with the request |
| `created_day` | Date extracted from `created_date` |
| `created_month` | Month extracted from `created_date` |
| `created_hour` | Hour of day when the request was opened |
| `day_of_week` | Day name from the created timestamp |
| `is_weekend` | Boolean flag for weekend-created requests |
| `is_closed` | Boolean flag indicating whether the request is closed |
| `resolution_hours` | Hours between created and closed timestamps |
| `resolution_bucket` | Resolution speed category |
| `priority_flag` | Flag for urgent quality-of-life request categories |

## Reporting tables

| Table | Description |
|---|---|
| `service_requests` | Cleaned record-level table |
| `summary_by_borough` | Request volume, closure, priority, and average resolution metrics by borough |
| `summary_by_complaint` | Complaint-level request volume and resolution metrics |
| `daily_volume` | Request counts by created day |
| `hourly_volume` | Request counts by hour of day |
| `resolution_buckets` | Request counts by resolution speed bucket |
