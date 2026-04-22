import pandas as pd

TOP_PRODUCT_COLUMNS = [
    "item_id",
    "title",
    "price",
    "sales",
    "shop",
    "province",
    "style",
    "fabric",
    "fit",
]


def filter_sales_data(df, group_col):
    temp_df = df.dropna(subset=[group_col, "sales"]).copy()
    temp_df = temp_df[temp_df["sales"] > 0]
    return temp_df


def filter_price_data(df, group_col, lower_quantile=0.01, upper_quantile=0.99):
    temp_df = df.dropna(subset=[group_col, "price"]).copy()
    temp_df = temp_df[temp_df["price"] > 0]

    if temp_df.empty:
        return temp_df

    lower = temp_df["price"].quantile(lower_quantile)
    upper = temp_df["price"].quantile(upper_quantile)
    temp_df = temp_df[(temp_df["price"] >= lower) & (temp_df["price"] <= upper)]
    return temp_df


def sales_analysis(df, group_col):
    temp_df = filter_sales_data(df, group_col)
    result = (
        temp_df.groupby(group_col, as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
        .reset_index(drop=True)
    )
    return result


def price_analysis(df, group_col):
    temp_df = filter_price_data(df, group_col)
    result = (
        temp_df.groupby(group_col, as_index=False)["price"]
        .mean()
        .round(2)
        .rename(columns={"price": "avg_price"})
        .sort_values("avg_price", ascending=False)
        .reset_index(drop=True)
    )
    return result


def category_sales_analysis(df):
    return sales_analysis(df, "category")


def province_sales_analysis(df):
    return sales_analysis(df, "province")


def shop_sales_analysis(df):
    return sales_analysis(df, "shop")


def style_price_analysis(df):
    return price_analysis(df, "style")


def pattern_price_analysis(df):
    return price_analysis(df, "pattern")


def fabric_price_analysis(df):
    return price_analysis(df, "fabric")


def fit_price_analysis(df):
    return price_analysis(df, "fit")


def dataframe_to_records(df):
    normalized_df = df.where(pd.notna(df), None)
    return normalized_df.to_dict(orient="records")


def top_products_by_dimension(df, field, value, limit=10):
    normalized_value = str(value).strip()
    normalized_field = df[field].astype(str).str.strip()
    temp_df = df[normalized_field == normalized_value].copy()
    temp_df = temp_df.dropna(subset=["item_id", "title", "sales"])
    temp_df = temp_df[temp_df["sales"] > 0]
    temp_df = temp_df.drop_duplicates(subset=["item_id"])

    result = (
        temp_df.sort_values("sales", ascending=False)
        .head(limit)[TOP_PRODUCT_COLUMNS]
        .reset_index(drop=True)
    )
    return result


def top_products_by_category(df, category_name, limit=10):
    return top_products_by_dimension(df, "category", category_name, limit=limit)


def top_products_by_province(df, province_name, limit=10):
    return top_products_by_dimension(df, "province", province_name, limit=limit)


def top_products_for_top_categories(df, category_limit=10, product_limit=10):
    category_sales_df = category_sales_analysis(df).head(category_limit)

    result = {}
    for category_name in category_sales_df["category"]:
        category_df = top_products_by_category(
            df,
            category_name=category_name,
            limit=product_limit,
        )
        result[category_name] = dataframe_to_records(category_df)

    return result


def top_products_for_top_provinces(df, province_limit=10, product_limit=10):
    province_sales_df = province_sales_analysis(df).head(province_limit)

    result = {}
    for province_name in province_sales_df["province"]:
        province_df = top_products_by_province(
            df,
            province_name=province_name,
            limit=product_limit,
        )
        result[province_name] = dataframe_to_records(province_df)

    return result


def run_all_analysis(df):
    return {
        "category_sales": category_sales_analysis(df),
        "province_sales": province_sales_analysis(df),
        "shop_sales": shop_sales_analysis(df),
        "style_price": style_price_analysis(df),
        "pattern_price": pattern_price_analysis(df),
        "fabric_price": fabric_price_analysis(df),
        "fit_price": fit_price_analysis(df),
    }
