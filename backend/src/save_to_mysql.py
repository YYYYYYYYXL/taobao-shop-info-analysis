import pandas as pd
from sqlalchemy import create_engine
import pymysql

# 连接数据库
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/taobao")

# 读取清洗数据
df = pd.read_csv("../data/cleaned_data.csv")

# 写入数据库
df.to_sql("cleaned_data", con=engine, if_exists="replace", index=False)
