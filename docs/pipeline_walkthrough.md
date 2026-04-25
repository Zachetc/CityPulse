# Pipeline Walkthrough

CityPulse ETL follows a standard extract, transform, validate, load, and report pattern.

## 1. Extract

`scripts/run_pipeline.py` starts by reading `data/raw/sample_311_service_requests.csv` through `src/extract.py`.

The input is a local CSV so the project stays reproducible. This avoids relying on a paid, rate-limited, or unstable external source while preserving the structure of a real ingestion pipeline.

## 2. Transform

`src/transform.py` standardizes the raw service request records.

It handles:

- date parsing
- borough normalization
- status normalization
- missing value cleanup
- complaint text formatting
- resolution-time calculation

It also creates derived fields:

- `created_day`
- `created_month`
- `created_hour`
- `day_of_week`
- `is_weekend`
- `is_closed`
- `resolution_hours`
- `resolution_bucket`
- `priority_flag`

## 3. Data quality

`src/data_quality.py` runs practical checks before the data is treated as analysis-ready.

Current checks include:

- raw row count
- cleaned row count
- duplicate request IDs
- missing created dates
- negative resolution times
- unknown borough share

The report is written to:

```text
outputs/data_quality_report.csv
```

## 4. PostgreSQL load

`src/load.py` loads the cleaned dataset and summary tables into PostgreSQL.

The database can be started locally with:

```bash
docker compose up -d
```

The loader creates:

- `service_requests`
- `summary_by_borough`
- `summary_by_complaint`
- `daily_volume`
- `hourly_volume`
- `resolution_buckets`

Indexes are added for fields that are commonly used in analysis queries.

## 5. Reporting

`src/reporting.py` creates charts and a text summary of the latest run.

Generated outputs include:

- requests by borough
- top complaint types
- daily request volume
- resolution bucket distribution
- pipeline summary text

The project also includes diagram assets used in the README:

- `assets/etl_architecture.png`
- `assets/postgres_schema.png`

## 6. SQL analysis

Reusable analysis queries are stored in:

```text
sql/example_analysis_queries.sql
```

`scripts/query_database.py` also demonstrates how to query the PostgreSQL tables from Python.
