from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


def load_to_csv(df: pd.DataFrame, path: Path) -> str:
    """Save the cleaned dataset as a CSV for easy inspection and database loading."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return str(path)


def _normalize_value(value):
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def _create_table_sql(table_name: str, df: pd.DataFrame) -> str:
    """Build a simple PostgreSQL table definition from a pandas DataFrame.

    This stays intentionally lightweight for a focused local prototype. In a larger
    system, I would use migrations with Alembic or dbt models instead.
    """
    type_map = {
        "int64": "BIGINT",
        "int32": "INTEGER",
        "float64": "DOUBLE PRECISION",
        "bool": "BOOLEAN",
        "datetime64[ns]": "TIMESTAMP",
    }
    columns = []
    for column, dtype in df.dtypes.items():
        pg_type = type_map.get(str(dtype), "TEXT")
        columns.append(f'"{column}" {pg_type}')
    return f'DROP TABLE IF EXISTS "{table_name}"; CREATE TABLE "{table_name}" ({", ".join(columns)});'


def _insert_dataframe(conn, table_name: str, df: pd.DataFrame) -> None:
    if df.empty:
        return
    columns = list(df.columns)
    rows = [tuple(_normalize_value(value) for value in row) for row in df.to_numpy()]
    column_sql = ", ".join(f'"{column}"' for column in columns)
    insert_sql = f'INSERT INTO "{table_name}" ({column_sql}) VALUES %s'
    with conn.cursor() as cur:
        cur.execute(_create_table_sql(table_name, df))
        execute_values(cur, insert_sql, rows)


def _create_indexes(conn) -> None:
    index_sql = [
        'CREATE INDEX IF NOT EXISTS idx_requests_borough ON service_requests(borough);',
        'CREATE INDEX IF NOT EXISTS idx_requests_day ON service_requests(created_day);',
        'CREATE INDEX IF NOT EXISTS idx_requests_complaint ON service_requests(complaint_type);',
        'CREATE INDEX IF NOT EXISTS idx_requests_status ON service_requests(status);',
    ]
    with conn.cursor() as cur:
        for statement in index_sql:
            cur.execute(statement)


def load_to_postgres(clean_df: pd.DataFrame, summaries: dict[str, pd.DataFrame], dsn: str) -> str:
    """Load cleaned service-request data and reporting aggregates into PostgreSQL."""
    with psycopg2.connect(dsn) as conn:
        _insert_dataframe(conn, "service_requests", clean_df)
        for table_name, table_df in summaries.items():
            _insert_dataframe(conn, table_name, table_df)
        _create_indexes(conn)
    return "postgresql://<user>:<password>@<host>:<port>/<database>"
