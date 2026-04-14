import pandas as pd
from data_analysis import run_all_analysis
from save_analysis_to_mysql import save_analysis_results


def main():
    df = pd.read_csv("../data/cleaned_data.csv")

    results = run_all_analysis(df)

    save_analysis_results(results)

    print("分析完成并已入库")


if __name__ == "__main__":
    main()
