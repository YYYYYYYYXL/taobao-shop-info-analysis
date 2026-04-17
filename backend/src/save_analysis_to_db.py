import pandas as pd
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from .config import get_engine

def validate_analysis_results(results: dict) -> None:
    if not isinstance(results, dict):
        raise TypeError("results 必须是字典类型")

    if not results:
        raise ValueError("分析结果为空，禁止入库")

    for table_name, result_df in results.items():
        if not isinstance(table_name, str) or not table_name.strip():
            raise ValueError("分析结果中的表名无效")

        if not isinstance(result_df, pd.DataFrame):
            raise TypeError(f"{table_name} 对应的结果必须是 pandas DataFrame")

        if result_df.empty:
            raise ValueError(f"{table_name} 的分析结果为空，禁止入库")
        


def save_analysis_results(results: dict, if_exists: str = "replace", chunksize: int = 1000) -> dict:
    start_time = datetime.now()
    
    try:
        validate_analysis_results(results)
        engine = get_engine()

        total_tables = 0
        total_rows = 0

        for table_name, result_df in results.items():
            result_df.to_sql(
                name=table_name,
                con=engine,
                if_exists=if_exists,
                index=False,
                chunksize=chunksize,
            )
            total_tables += 1
            total_rows += len(result_df)

        end_time = datetime.now()
        return {
            "success": True,
            "table_count": total_tables,
            "row_count": int(total_rows),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": round((end_time - start_time).total_seconds(), 3),
            "message": "分析结果入库成功",
        }

    except (TypeError, ValueError) as exc:
        end_time = datetime.now()
        return {
            "success": False,
            "table_count": 0,
            "row_count": 0,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": round((end_time - start_time).total_seconds(), 3),
            "message": f"分析结果校验失败: {exc}",
        }

    except SQLAlchemyError as exc:
        end_time = datetime.now()
        return {
            "success": False,
            "table_count": 0,
            "row_count": 0,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": round((end_time - start_time).total_seconds(), 3),
            "message": f"分析结果入库失败: {exc}",
        }        