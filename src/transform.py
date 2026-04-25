from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = {"unique_key", "created_date", "closed_date", "agency", "complaint_type", "borough", "status"}
BOROUGH_NORMALIZATION = {"MANHATTAN": "MANHATTAN", "NEW YORK": "MANHATTAN", "BRONX": "BRONX", "BROOKLYN": "BROOKLYN", "KINGS": "BROOKLYN", "QUEENS": "QUEENS", "STATEN ISLAND": "STATEN ISLAND", "RICHMOND": "STATEN ISLAND"}


def validate_columns(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def _clean_text(series: pd.Series) -> pd.Series:
    return series.fillna("UNKNOWN").astype(str).str.strip().str.upper().replace({"": "UNKNOWN", "NAN": "UNKNOWN"})


def transform_requests(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich service request records using readable Pandas steps."""
    validate_columns(df)
    cleaned = df.copy()
    cleaned["created_date"] = pd.to_datetime(cleaned["created_date"], errors="coerce")
    cleaned["closed_date"] = pd.to_datetime(cleaned["closed_date"], errors="coerce")

    for col in ["agency", "complaint_type", "descriptor", "borough", "status"]:
        if col in cleaned.columns:
            cleaned[col] = _clean_text(cleaned[col])

    cleaned["borough"] = cleaned["borough"].map(BOROUGH_NORMALIZATION).fillna(cleaned["borough"])
    cleaned["incident_zip"] = cleaned.get("incident_zip", pd.Series(index=cleaned.index, dtype="object"))
    cleaned["incident_zip"] = cleaned["incident_zip"].fillna("UNKNOWN").astype(str).str.replace(".0", "", regex=False)

    cleaned = cleaned.dropna(subset=["created_date"])
    cleaned = cleaned.drop_duplicates(subset=["unique_key"], keep="first")
    cleaned["created_day"] = cleaned["created_date"].dt.date.astype(str)
    cleaned["created_month"] = cleaned["created_date"].dt.to_period("M").astype(str)
    cleaned["created_hour"] = cleaned["created_date"].dt.hour
    cleaned["day_of_week"] = cleaned["created_date"].dt.day_name()
    cleaned["is_weekend"] = cleaned["created_date"].dt.dayofweek.isin([5, 6])
    cleaned["is_closed"] = cleaned["closed_date"].notna() | cleaned["status"].eq("CLOSED")

    cleaned["resolution_hours"] = ((cleaned["closed_date"] - cleaned["created_date"]).dt.total_seconds() / 3600).round(2)
    cleaned.loc[cleaned["resolution_hours"] < 0, "resolution_hours"] = pd.NA
    cleaned["resolution_bucket"] = pd.cut(cleaned["resolution_hours"], bins=[-0.01, 24, 72, 168, float("inf")], labels=["same_day", "1_to_3_days", "4_to_7_days", "over_7_days"]).astype("object").fillna("open_or_unknown")
    cleaned["priority_flag"] = cleaned["complaint_type"].str.contains("HEAT|HOT WATER|NOISE|BLOCKED|FLOOD|WATER|ELECTRIC|SAFETY", regex=True, na=False)
    return cleaned.sort_values(["created_date", "unique_key"]).reset_index(drop=True)


def build_summary_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    by_borough = df.groupby("borough", dropna=False).agg(request_count=("unique_key", "count"), closed_count=("is_closed", "sum"), priority_count=("priority_flag", "sum"), avg_resolution_hours=("resolution_hours", "mean")).reset_index()
    by_borough["closed_rate_pct"] = (by_borough["closed_count"] / by_borough["request_count"] * 100).round(2)
    by_borough["avg_resolution_hours"] = by_borough["avg_resolution_hours"].round(2)
    by_complaint = df.groupby("complaint_type", dropna=False).agg(request_count=("unique_key", "count"), avg_resolution_hours=("resolution_hours", "mean"), priority_count=("priority_flag", "sum")).reset_index().sort_values("request_count", ascending=False)
    by_complaint["avg_resolution_hours"] = by_complaint["avg_resolution_hours"].round(2)
    daily_volume = df.groupby("created_day", dropna=False).size().reset_index(name="request_count")
    hourly_volume = df.groupby("created_hour", dropna=False).size().reset_index(name="request_count").sort_values("created_hour")
    resolution_buckets = df.groupby("resolution_bucket", dropna=False).size().reset_index(name="request_count").sort_values("request_count", ascending=False)
    return {"summary_by_borough": by_borough, "summary_by_complaint": by_complaint, "daily_volume": daily_volume, "hourly_volume": hourly_volume, "resolution_buckets": resolution_buckets}
