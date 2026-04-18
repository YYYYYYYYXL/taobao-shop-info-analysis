import re
from pathlib import Path

import pandas as pd

from .config import CLEANED_CSV_PATH, RAW_CSV_PATH


STYLE_MAP = {
    "中式": "中式风",
    "中性": "中性风",
    "休闲": "休闲风",
    "优雅": "优雅风",
    "公主": "公主风",
    "可爱": "可爱风",
    "复古": "复古风",
    "学院": "学院风",
    "工装": "工装风",
    "性感": "性感风",
    "文艺": "文艺风",
    "欧美": "欧美风",
    "淑女": "淑女风",
    "甜美": "甜美风",
    "简约": "简约风",
    "英伦": "英伦风",
    "街头": "街头风",
    "运动": "运动风",
    "通勤": "通勤风",
}

FABRIC_MAP = {
    "全棉": "棉",
    "纯棉": "棉",
    "纯棉(棉含量100%)": "棉",
    "棉100%": "棉",
    "棉质面料": "棉",
    "棉": "棉",
    "精梳棉": "棉",
    "莱卡棉": "棉",
    "丝光棉": "棉",
    "涤纶": "聚酯纤维",
    "涤纶（聚酯纤维）": "聚酯纤维",
    "聚酯纤维100%": "聚酯纤维",
    "聚酯纤维（涤纶）": "聚酯纤维",
    "粘纤": "粘胶纤维",
    "粘胶": "粘胶纤维",
    "粘胶纤维（粘纤）": "粘胶纤维",
    "莫代尔纤维": "莫代尔",
    "聚氨酯弹性纤维(氨纶)": "聚氨酯弹性纤维",
    "聚氨酯弹性纤维（氨纶）": "聚氨酯弹性纤维",
    "PU皮": "PU",
}

FIT_MAP = {
    "修身型": "修身",
    "宽松型": "宽松",
    "收腰型": "收腰",
    "直筒型": "直筒",
}

SEASON_MAP = {
    "春天": "春季",
    "夏天": "夏季",
    "秋天": "秋季",
    "冬天": "冬季",
    "秋冬季": "秋冬",
}

COLUMN_MAPPING = {
    "商品id": "item_id",
    "分类": "category",
    "商品标题": "title",
    "商品价格": "price",
    "省份": "province",
    "商品销量": "sales",
    "店铺名称": "shop",
    "店铺标签": "shop_tag",
    "先用后付": "pay_later",
    "退货宝": "return_flag",
    "风格": "style",
    "款式": "pattern",
    "面料": "fabric",
    "版型": "fit",
    "适用季节": "season",
}

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


def parse_sales(value):
    if pd.isna(value):
        return None

    text = str(value).strip()
    match = re.fullmatch(r"(\d+(?:\.\d+)?)(万)?\+?人付款", text)
    if not match:
        return None

    amount = float(match.group(1))
    if match.group(2):
        amount *= 10000
    return int(amount)

 
def load_raw_data(input_path: str | Path) -> pd.DataFrame:
    path = Path(input_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"raw data file not found: {path}")

    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"raw data is empty: {path}")

    df.columns = [str(column).strip() for column in df.columns]
    return df.rename(columns=COLUMN_MAPPING)


def validate_schema(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("raw dataframe is empty")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"missing required columns: {missing_columns}")

    duplicated_columns = df.columns[df.columns.duplicated()].tolist()
    if duplicated_columns:
        raise ValueError(f"duplicated columns: {duplicated_columns}")


def clean_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    cleaned = df.copy()
    metrics = {
        "before_rows": int(len(cleaned)),
        "price_invalid_rows": 0,
        "sales_invalid_rows": 0,
        "after_rows": 0,
        "dropped_rows": 0,
    }

    cleaned["item_id"] = cleaned["item_id"].astype(str).str.replace(r"\s+", "", regex=True)
    cleaned["title"] = cleaned["title"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
    cleaned["shop"] = cleaned["shop"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)

    cleaned["price"] = pd.to_numeric(cleaned["price"], errors="coerce")
    price_valid_mask = cleaned["price"].notna() & (cleaned["price"] > 0)
    metrics["price_invalid_rows"] = int((~price_valid_mask).sum())

    cleaned["sales"] = cleaned["sales"].apply(parse_sales)
    sales_valid_mask = cleaned["sales"].notna() & (cleaned["sales"] > 0)
    metrics["sales_invalid_rows"] = int((~sales_valid_mask).sum())

    cleaned = cleaned[price_valid_mask & sales_valid_mask].copy()
    cleaned["style"] = cleaned["style"].replace(STYLE_MAP)
    cleaned["fabric"] = cleaned["fabric"].replace(FABRIC_MAP)
    cleaned["fit"] = cleaned["fit"].replace(FIT_MAP)
    cleaned["season"] = cleaned["season"].replace(SEASON_MAP)

    metrics["after_rows"] = int(len(cleaned))
    metrics["dropped_rows"] = metrics["before_rows"] - metrics["after_rows"]
    return cleaned, metrics


def save_cleaned(cleaned_df: pd.DataFrame, output_path: str | Path):
    output = Path(output_path).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output, index=False, encoding="utf-8-sig")
    return output


def summarize_cleaning(input_path, output_path, metrics):
    return {
        "input_path": str(input_path),
        "output_path": str(output_path),
        "before_rows": int(metrics["before_rows"]),
        "after_rows": int(metrics["after_rows"]),
        "dropped_rows": int(metrics["dropped_rows"]),
        "price_invalid_rows": int(metrics["price_invalid_rows"]),
        "sales_invalid_rows": int(metrics["sales_invalid_rows"]),
    }


def main() -> dict:
    raw_df = load_raw_data(RAW_CSV_PATH)
    validate_schema(raw_df)
    cleaned_df, metrics = clean_dataframe(raw_df)
    output_path = save_cleaned(cleaned_df, CLEANED_CSV_PATH)
    return summarize_cleaning(RAW_CSV_PATH, output_path, metrics)


if __name__ == "__main__":
    print(main())
