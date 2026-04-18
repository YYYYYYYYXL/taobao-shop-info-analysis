import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

RAW_CSV_PATH = (BASE_DIR / os.getenv("RAW_CSV_PATH", "data/淘宝电商数据集.csv")).resolve()
CLEANED_CSV_PATH = (BASE_DIR / os.getenv("CLEANED_CSV_PATH", "data/cleaned_data.csv")).resolve()
