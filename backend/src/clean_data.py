def parse_sales(x):
    if pd.isna(x):
        return None

    s = str(x).strip()
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(万?\+?人付款)", s)

    if not m:
        return None

    num = float(m.group(1))
    if m.group(2).startswith("万"):
        num *= 10000

    return int(num)

style_map = {
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

fabric_map = {
    "全棉": "棉",
    "纯棉": "棉",
    "纯棉(棉含量100%)": "棉",
    "棉100%": "棉",
    "棉质面料": "棉",
    "绵": "棉",
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


fit_map = {
    "修身型": "修身",
    "宽松型": "宽松",
    "收腰型": "收腰",
    "直筒型": "直筒",
}


season_map = {
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

import pandas as pd
from pathlib import Path 
import re
from datetime import datetime
from .config import RAW_CSV_PATH, CLEANED_CSV_PATH

def load_raw_data(input_path: str | Path) -> pd.DataFrame:
    path = Path(input_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"未找到原始数据文件: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"无法读取 csv 文件: {path}") from e

    if df.empty:
        raise ValueError(f"原始数据为空: {path}")

    df.columns = [str(c).strip() for c in df.columns]
    df = df.rename(columns=COLUMN_MAPPING)

    return df

def validate_schema(df, strict=True):
    """DataFrame 列结构校验"""
    """ 严格模式（stric=True）：issues = 临时攒错的小本子 → 攒齐一次性报错，用完就扔
        宽松模式：issues = 给你用的问题清单 → 返回给你查看、处理
    """
    required_cols = [
        "item_id", "category", "title", "price", "province", "sales",
        "shop", "shop_tag", "pay_later", "return_flag",
        "style", "pattern", "fabric", "fit", "season",
    ]
    issues = []    #问题列表

    if df.empty:
        issues.append("DataFrame 是空的")

    missing = [c for c in required_cols if c not in df.columns]    #存入缺失列的列名
    if missing:    #missing空的话就是没有缺失列
        issues.append(f"缺少必要列: {missing}")

    duplicated_cols = df.columns[df.columns.duplicated()].tolist()     #df.columns.duplicated()：查列名重复，打 True/False 标记，把 Pandas 的Index对象 → 转成普通 Python 列表
    if duplicated_cols:
        issues.append(f"重复的列: {duplicated_cols}")

    if strict and issues:
        raise ValueError(" | ".join(issues))
    return issues


def clean_dataframe(df) -> tuple[pd.DataFrame, dict]:
    """清洗数据"""
    cleaned = df.copy()     #拷贝元数据生成新副本cleaned
    metrics = {
        "before_rows":len(cleaned),
        "sales_invalid_rows":0,
        "price_invalid_rows":0
    }

    cleaned["item_id"] = cleaned["item_id"].astype(str).str.replace(r"\s+", "", regex=True)
    cleaned["title"] = cleaned["title"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
    cleaned["shop"] = cleaned["shop"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
    #price
    cleaned["price"] = pd.to_numeric(cleaned["price"], errors="coerce")
    price_valid_mask = cleaned["price"].notna() & (cleaned["price"] > 0)
    metrics["price_invalid_rows"] = int((~price_valid_mask).sum())
    #sales
    cleaned["sales"] = cleaned["sales"].apply(parse_sales)
    sales_valid_mask = cleaned["sales"].notna() & (cleaned["sales"] > 0)
    metrics["sales_invalid_rows"] = int((~sales_valid_mask).sum())
    
    cleaned = cleaned[price_valid_mask & sales_valid_mask].copy()

    cleaned["style"] = cleaned["style"].replace(style_map)
    cleaned["fabric"] = cleaned["fabric"].replace(fabric_map)
    cleaned["fit"] = cleaned["fit"].replace(fit_map)
    cleaned["season"] = cleaned["season"].replace(season_map)

    metrics["after_rows"] = len(cleaned)
    metrics["dropped_rows"] = metrics["before_rows"] - metrics["after_rows"]
    return cleaned,metrics



def save_cleaned(cleaned_df, output_path):
    """保存清理后的数据"""
    output = Path(output_path).expanduser().resolve()    
    output.parent.mkdir(parents=True, exist_ok=True)    #output.parent：这个文件的「上级文件夹」，parents=True：递归创建文件夹，exist_ok=True：文件夹已存在也不报错

    cleaned_df.to_csv(output, index=False, encoding="utf-8-sig")
    return output


def build_report(input_path, output_path, metrics, start_ts, end_ts, schema_issues=None):
    """标准化的运行报告"""
    schema_issues = schema_issues or []
    report = {
        "success": True,
        "run_started_at": start_ts.isoformat(),
        "run_finished_at": end_ts.isoformat(),
        "duration_seconds": round((end_ts - start_ts).total_seconds(), 3),
        "input_path": str(input_path),
        "output_path": str(output_path),
        "metrics": {
            "before_rows": int(metrics.get("before_rows", 0)),
            "after_rows": int(metrics.get("after_rows", 0)),
            "dropped_rows": int(metrics.get("dropped_rows", 0)),
            "sales_invalid_rows": int(metrics.get("sales_invalid_rows", 0)),
            "price_invalid_rows": int(metrics.get("price_invalid_rows", 0)),
        },
        "schema_issues": schema_issues,
    }
    return report

def main() -> dict:
      start_time = datetime.now()

      raw_df = load_raw_data(RAW_CSV_PATH)
      schema_issues = validate_schema(raw_df, strict=False)

      if schema_issues:
          raise ValueError(f"原始数据字段校验未通过: {schema_issues}")

      cleaned_df, metrics = clean_dataframe(raw_df)
      output_path = save_cleaned(cleaned_df, CLEANED_CSV_PATH)

      end_time = datetime.now()

      return build_report(
          input_path=RAW_CSV_PATH,
          output_path=output_path,
          metrics=metrics,
          start_ts=start_time,
          end_ts=end_time,
          schema_issues=schema_issues,
      )

if __name__ == "__main__":
      report = main()
      print(report)