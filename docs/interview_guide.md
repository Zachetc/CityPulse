# Project Explanation Guide

## One-minute explanation

CityPulse ETL is a PostgreSQL-backed data pipeline for analyzing 311-style city service requests. It extracts raw CSV records, cleans and standardizes the data with Python and Pandas, runs validation checks, loads the results into PostgreSQL, and creates reporting tables and visuals for operational analysis.

The goal was to build a practical data engineering project around a real public-sector analytics problem: service requests are messy, timestamp-heavy, and useful only after standardization and aggregation.

## Why the project changed from transit data

The original idea was to build an MTA ridership ETL pipeline. After looking into available data sources, I found that consistent ridership data was either difficult to access, fragmented, or not ideal for a reproducible local portfolio project.

Rather than force a brittle data source, I kept the same engineering pattern and shifted the domain to city service requests. The core ETL work is similar: ingest public-sector operational data, clean it, validate it, model it relationally, and create reporting outputs.

## Why PostgreSQL

PostgreSQL makes the project more realistic than a CSV-only workflow because most analytics pipelines eventually land cleaned data in a relational database.

This project uses PostgreSQL to demonstrate:

- database connection configuration
- local database setup through Docker
- table creation and loading
- indexes for analysis queries
- reusable SQL reporting patterns

## Main pipeline steps

1. **Extract** raw service request records from CSV.
2. **Transform** timestamps, borough names, statuses, and complaint fields.
3. **Engineer fields** such as resolution time, request hour, weekend flag, and priority flag.
4. **Validate data quality** with row counts, duplicate checks, missing date checks, and invalid resolution-time checks.
5. **Load to PostgreSQL** as cleaned record-level and summary tables.
6. **Report** through SQL queries, charts, and a run summary.

## Design tradeoffs

I intentionally kept the pipeline modular but not overengineered.

- I used Pandas because it is readable and appropriate for the current dataset size.
- I used PostgreSQL instead of SQLite to make the database layer more realistic.
- I used Docker Compose so the project can be started without manually installing a database.
- I kept orchestration out of scope because the goal was to first build a clean, explainable ETL foundation.

## What I would improve next

If I continued developing this project, I would add:

- incremental loading based on request ID or created date
- scheduled ingestion from NYC Open Data
- dbt models for reporting tables
- GitHub Actions for automated tests
- a dashboard for trend exploration
- stronger validation using Pandera or Great Expectations

## Questions I should be ready to answer

1. Why did you move away from MTA ridership data?
2. What does each ETL layer do?
3. How are service request records cleaned?
4. How is resolution time calculated?
5. What data quality checks are included?
6. Why use PostgreSQL instead of only CSVs?
7. What indexes are created and why?
8. How would this scale to millions of records?
9. What would change in a production version?
10. How would you add incremental loading?
