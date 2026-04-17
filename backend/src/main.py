from datetime import datetime

from .analyze_data import run_all_analysis
from .clean_data import build_report, clean_dataframe, load_raw_data, save_cleaned, validate_schema
from .config import CLEANED_CSV_PATH, RAW_CSV_PATH


def main() -> dict:
    start_time = datetime.now()

    raw_df = load_raw_data(RAW_CSV_PATH)
    schema_issues = validate_schema(raw_df, strict=False)
    if schema_issues:
        raise ValueError(f"raw data schema validation failed: {schema_issues}")

    cleaned_df, metrics = clean_dataframe(raw_df)
    output_path = save_cleaned(cleaned_df, CLEANED_CSV_PATH)
    analysis_results = run_all_analysis(cleaned_df)

    report = build_report(
        input_path=RAW_CSV_PATH,
        output_path=output_path,
        metrics=metrics,
        start_ts=start_time,
        end_ts=datetime.now(),
        schema_issues=schema_issues,
    )
    report["analysis_tables"] = {key: int(len(value)) for key, value in analysis_results.items()}
    report["message"] = "cleaning and analysis completed from local CSV"
    return report


if __name__ == "__main__":
    print(main())
