from __future__ import annotations

import pandas as pd
import psycopg2

from src.config import postgres_dsn

QUERIES = {
    "borough_summary": """
        SELECT borough, request_count, closed_rate_pct, avg_resolution_hours
        FROM summary_by_borough
        ORDER BY request_count DESC;
    """,
    "top_complaints": """
        SELECT complaint_type, request_count, avg_resolution_hours
        FROM summary_by_complaint
        ORDER BY request_count DESC
        LIMIT 10;
    """,
    "priority_flags": """
        SELECT unique_key, borough, complaint_type, resolution_hours
        FROM service_requests
        WHERE priority_flag = TRUE
        ORDER BY resolution_hours DESC
        LIMIT 10;
    """,
}


def run_query(name: str) -> pd.DataFrame:
    if name not in QUERIES:
        raise ValueError(f"Unknown query '{name}'. Options: {list(QUERIES)}")
    with psycopg2.connect(postgres_dsn()) as conn:
        return pd.read_sql_query(QUERIES[name], conn)


if __name__ == "__main__":
    for query_name in QUERIES:
        print(f"\n--- {query_name} ---")
        print(run_query(query_name).to_string(index=False))
