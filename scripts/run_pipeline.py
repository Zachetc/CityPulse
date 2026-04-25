from src.config import (
    ASSETS_DIR,
    DATA_QUALITY_REPORT_PATH,
    OUTPUT_DIR,
    PIPELINE_SUMMARY_PATH,
    PROCESSED_DATA_PATH,
    RAW_DATA_PATH,
    postgres_dsn,
)
from src.data_quality import build_quality_report, save_quality_report
from src.extract import extract_csv
from src.load import load_to_csv, load_to_postgres
from src.reporting import (
    save_bar_chart,
    save_line_chart,
    save_pipeline_architecture,
    save_postgres_schema_diagram,
    write_pipeline_summary,
)
from src.transform import build_summary_tables, transform_requests


def main() -> None:
    raw_df = extract_csv(RAW_DATA_PATH)
    clean_df = transform_requests(raw_df)
    summaries = build_summary_tables(clean_df)
    quality_report = build_quality_report(raw_df, clean_df)

    clean_csv = load_to_csv(clean_df, PROCESSED_DATA_PATH)
    database_target = load_to_postgres(clean_df, summaries, postgres_dsn())
    quality_csv = save_quality_report(quality_report, DATA_QUALITY_REPORT_PATH)

    save_bar_chart(summaries["summary_by_borough"].sort_values("request_count", ascending=False), "borough", "request_count", "Service Requests by Borough", OUTPUT_DIR / "requests_by_borough.png")
    save_bar_chart(summaries["summary_by_complaint"].head(10), "complaint_type", "request_count", "Top Complaint Types", OUTPUT_DIR / "top_complaint_types.png")
    save_line_chart(summaries["daily_volume"], "created_day", "request_count", "Daily Service Request Volume", OUTPUT_DIR / "daily_request_volume.png")
    save_bar_chart(summaries["resolution_buckets"], "resolution_bucket", "request_count", "Resolution Time Buckets", OUTPUT_DIR / "resolution_buckets.png")
    save_pipeline_architecture(ASSETS_DIR / "etl_architecture.png")
    save_postgres_schema_diagram(ASSETS_DIR / "postgres_schema.png")
    summary_txt = write_pipeline_summary(clean_df, quality_report, PIPELINE_SUMMARY_PATH)

    print(f"Loaded {len(clean_df)} service request records")
    print(f"Clean CSV: {clean_csv}")
    print(f"PostgreSQL target: {database_target}")
    print(f"Data quality report: {quality_csv}")
    print(f"Run summary: {summary_txt}")
    print(f"Charts written to: {OUTPUT_DIR}")
    print(f"README diagrams written to: {ASSETS_DIR}")


if __name__ == "__main__":
    main()
