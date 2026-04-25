from __future__ import annotations

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = ROOT_DIR / "outputs"
DOCS_DIR = ROOT_DIR / "docs"
ASSETS_DIR = ROOT_DIR / "assets"

RAW_DATA_PATH = RAW_DIR / "sample_311_service_requests.csv"
PROCESSED_DATA_PATH = PROCESSED_DIR / "service_requests_clean.csv"
DATA_QUALITY_REPORT_PATH = OUTPUT_DIR / "data_quality_report.csv"
PIPELINE_SUMMARY_PATH = OUTPUT_DIR / "pipeline_summary.txt"

# PostgreSQL connection settings. Defaults work with docker-compose.yml.
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "city_requests")
POSTGRES_USER = os.getenv("POSTGRES_USER", "city_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "city_password")


def postgres_dsn() -> str:
    """Return a psycopg2-compatible DSN string."""
    return (
        f"host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DB} "
        f"user={POSTGRES_USER} password={POSTGRES_PASSWORD}"
    )


for folder in [RAW_DIR, PROCESSED_DIR, OUTPUT_DIR, DOCS_DIR, ASSETS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)
