from .analyze_data import run_all_analysis
from .clean_data import clean_dataframe, load_raw_data, save_cleaned, summarize_cleaning, validate_schema
from .config import CLEANED_CSV_PATH, RAW_CSV_PATH


def main() -> dict:
    raw_df = load_raw_data(RAW_CSV_PATH)
    validate_schema(raw_df)

    cleaned_df, metrics = clean_dataframe(raw_df)
    output_path = save_cleaned(cleaned_df, CLEANED_CSV_PATH)
    analysis_results = run_all_analysis(cleaned_df)

    return {
        "message": "cleaning and analysis completed",
        "cleaning": summarize_cleaning(RAW_CSV_PATH, output_path, metrics),
        "analysis_tables": {key: int(len(value)) for key, value in analysis_results.items()},
    }


if __name__ == "__main__":
    print(main())
