import pandas as pd
import re

df = pd.read_csv("../data/淘宝电商数据集.csv")
df.columns = [
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

# 1. item_id：转字符串，去所有空白字符
df["item_id"] = df["item_id"].astype(str).str.replace(r"\s+", "", regex=True)

# 2. title：去首尾空白，连续空白压成一个空格
df["title"] = df["title"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)

# 3. price：当前数据可直接严格转数值，失败就报错
df["price"] = pd.to_numeric(df["price"], errors="raise")


# 4. sales：按真实格式解析，例如 6000+人付款 / 6万+人付款 / 30人付款
def parse_sales(x):
    if pd.isna(x):
        return x
    s = str(x).strip()
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(万)?\+?人付款", s)
    if not m:
        raise ValueError(f"无法解析的销量值: {s}")
    num = float(m.group(1))
    if m.group(2) == "万":
        num *= 10000
    return int(num)


df["sales"] = df["sales"].apply(parse_sales)
df = df[(df["sales"].notna()) & (df["sales"] > 0)]

# 5. shop：去首尾空白，连续空白压成一个空格
df["shop"] = df["shop"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)

# 6. style：按数据里真实存在的同义值统一
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
df["style"] = df["style"].replace(style_map)

# 7. fabric：按数据里真实存在的同义值统一
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
df["fabric"] = df["fabric"].replace(fabric_map)

# 8. fit：按真实存在的同义值统一
fit_map = {
    "修身型": "修身",
    "宽松型": "宽松",
    "收腰型": "收腰",
    "直筒型": "直筒",
}
df["fit"] = df["fit"].replace(fit_map)

# 9. season：按真实存在的同义值统一
season_map = {
    "春天": "春季",
    "夏天": "夏季",
    "秋天": "秋季",
    "冬天": "冬季",
    "秋冬季": "秋冬",
}
df["season"] = df["season"].replace(season_map)


df.to_csv("../data/cleaned_data.csv", index=False, encoding="utf-8-sig")
