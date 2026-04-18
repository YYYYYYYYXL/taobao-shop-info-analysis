import pandas as pd


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
