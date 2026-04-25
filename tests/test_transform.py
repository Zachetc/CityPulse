import pandas as pd

from src.data_quality import build_quality_report
from src.transform import build_summary_tables, transform_requests


def sample_df():
    return pd.DataFrame({
        "unique_key": [1, 2, 3],
        "created_date": ["2025-01-01 08:00", "2025-01-01 09:00", "2025-01-02 10:00"],
        "closed_date": ["2025-01-01 12:00", None, "2025-01-03 10:00"],
        "agency": ["NYPD", "DEP", "HPD"],
        "complaint_type": ["Noise", "Water Leak", "Heat/Hot Water"],
        "descriptor": ["Loud Music", "Leak", "No Heat"],
        "borough": ["brooklyn", "NEW YORK", "queens"],
        "status": ["Closed", "Open", "Closed"],
        "incident_zip": [11201, 10001, None],
    })


def test_transform_creates_business_columns():
    clean = transform_requests(sample_df())
    assert "resolution_hours" in clean.columns
    assert "resolution_bucket" in clean.columns
    assert "priority_flag" in clean.columns
    assert clean.loc[0, "borough"] == "BROOKLYN"
    assert clean.loc[1, "borough"] == "MANHATTAN"


def test_summary_tables_include_expected_outputs():
    clean = transform_requests(sample_df())
    summaries = build_summary_tables(clean)
    assert "summary_by_borough" in summaries
    assert "hourly_volume" in summaries
    assert "resolution_buckets" in summaries
    assert summaries["summary_by_borough"]["request_count"].sum() == 3


def test_quality_report_flags_core_checks():
    raw = sample_df()
    clean = transform_requests(raw)
    report = build_quality_report(raw, clean)
    assert {"check", "value", "status", "notes"}.issubset(report.columns)
    assert "raw_row_count" in set(report["check"])
