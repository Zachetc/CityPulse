"""Small, explainable data-quality checks for the ETL pipeline."""
from __future__ import annotations
import pandas as pd


def build_quality_report(raw_df: pd.DataFrame, clean_df: pd.DataFrame) -> pd.DataFrame:
    checks = []
    def add_check(name: str, value, status: str, notes: str) -> None:
        checks.append({"check": name, "value": value, "status": status, "notes": notes})
    add_check("raw_row_count", len(raw_df), "pass" if len(raw_df) > 0 else "fail", "Raw file should contain records.")
    add_check("clean_row_count", len(clean_df), "pass" if len(clean_df) > 0 else "fail", "Cleaned dataset should contain valid records.")
    dupes = int(clean_df["unique_key"].duplicated().sum()) if "unique_key" in clean_df else -1
    add_check("duplicate_unique_keys", dupes, "pass" if dupes == 0 else "warn", "Unique request IDs should not repeat.")
    missing_dates = int(clean_df["created_date"].isna().sum()) if "created_date" in clean_df else -1
    add_check("missing_created_date", missing_dates, "pass" if missing_dates == 0 else "fail", "Created date is required.")
    negative = int((clean_df["resolution_hours"] < 0).sum()) if "resolution_hours" in clean_df else -1
    add_check("negative_resolution_hours", negative, "pass" if negative == 0 else "warn", "Negative resolution times indicate bad timestamps.")
    unknown_share = round(clean_df["borough"].eq("UNKNOWN").mean() * 100, 2) if "borough" in clean_df else -1
    add_check("unknown_borough_share_pct", unknown_share, "pass" if unknown_share <= 20 else "warn", "High UNKNOWN borough share weakens geographic reporting.")
    return pd.DataFrame(checks)


def save_quality_report(report: pd.DataFrame, path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(path, index=False)
    return str(path)
