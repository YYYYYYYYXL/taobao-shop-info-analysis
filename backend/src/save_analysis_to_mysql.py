from sqlalchemy import create_engine


def get_engine():
    engine = create_engine(
        "mysql+pymysql://root:123456@localhost:3306/taobao?charset=utf8mb4"
    )
    return engine


def save_analysis_results(results):
    engine = get_engine()

    for table_name, result_df in results.items():
        print(f"正在写入表: {table_name}")
        result_df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)

    print("所有分析结果已写入数据库")
