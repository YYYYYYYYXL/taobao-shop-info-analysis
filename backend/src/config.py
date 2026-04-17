import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


def require_env(key: str) -> str:
    value = os.getenv(key, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env: {key}")
    return value


def get_engine():
    return create_engine(require_env("MYSQL_URL"))


RAW_CSV_PATH = (BASE_DIR / os.getenv("RAW_CSV_PATH", "data/淘宝电商数据集.csv")).resolve()
CLEANED_CSV_PATH = (BASE_DIR / os.getenv("CLEANED_CSV_PATH", "data/cleaned_data.csv")).resolve()
CLEANED_TABLE = os.getenv("CLEANED_TABLE", "cleaned_data")
