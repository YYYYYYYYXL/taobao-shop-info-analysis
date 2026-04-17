from datetime import datetime

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from .config import CLEANED_TABLE, get_engine


REQUIRED_COLUMNS = [
    "item_id",
    "category",
    "title",
    "price",
    "province",
    "sales",
    "shop",
    "shop_tag",
    "pay_later",
    "return_flag",
    "style",
    "pattern",
    "fabric",
    "fit",
    "season",
]


def validate_cleaned_data(cleaned_df: pd.DataFrame) -> None:
    if not isinstance(cleaned_df, pd.DataFrame):
        raise TypeError("cleaned_df 必须是 pandas DataFrame")

    if cleaned_df.empty:
        raise ValueError("清洗后的数据为空，禁止入库")

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in cleaned_df.columns]
    if missing_columns:
        raise ValueError(f"清洗后的数据缺少必要字段: {missing_columns}")

    if cleaned_df["item_id"].isna().any():
        raise ValueError("item_id 存在空值，禁止入库")

    if cleaned_df["item_id"].astype(str).str.strip().eq("").any():
        raise ValueError("item_id 存在空字符串，禁止入库")



def save_cleaned_to_db(
    cleaned_df: pd.DataFrame,
    table_name: str = CLEANED_TABLE,
    if_exists: str = "replace",
    chunksize: int = 1000,
) -> dict:
    start_time = datetime.now()

    try:
        validate_cleaned_data(cleaned_df)
        engine = get_engine()

        cleaned_df.to_sql(
            name=table_name,
            con=engine,
            if_exists=if_exists,
            index=False,
            chunksize=chunksize,
        )

        end_time = datetime.now()
        return {
            "success": True,
            "table_name": table_name,
            "row_count": int(len(cleaned_df)),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": round((end_time - start_time).total_seconds(), 3),
            "message": "清洗后数据入库成功",
        }

    except (TypeError, ValueError) as exc:
        end_time = datetime.now()
        return {
            "success": False,
            "table_name": table_name,
            "row_count": 0,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": round((end_time - start_time).total_seconds(), 3),
            "message": f"数据校验失败: {exc}",
        }

    except SQLAlchemyError as exc:
        end_time = datetime.now()
        return {
            "success": False,
            "table_name": table_name,
            "row_count": 0,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": round((end_time - start_time).total_seconds(), 3),
            "message": f"数据库写入失败: {exc}",
        }
    