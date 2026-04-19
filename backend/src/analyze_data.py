import pandas as pd

#-----------------------------------------过滤函数-------------------------------------------------
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
#------------------------------------------------------------------------------------------------

#-----------------------------------------通用分析函数--------------------------------------------
def sales_analysis(df, group_col):    # 分析销售数据 根据指定的分组列（如类别、店铺、所在省份等）对销售数据进行分析 
    temp_df = filter_sales_data(df, group_col)  # 调用过滤函数，去除缺失值和销量为0的数据
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
#------------------------------------------------------------------------------------------------





#-----------------------------------------各维度分析函数--------------------------------------------
def category_sales_analysis(df):   #分析类别销售数据
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
#------------------------------------------------------------------------------------------------


#-----------------------------------------细致分类函数--------------------------------------------
def top_products_by_category(df, category_name, limit=10):
    temp_df = df[df["category"] == category_name].copy()
    temp_df = temp_df.dropna(subset=["item_id", "title", "sales"])

    temp_df = temp_df.drop_duplicates(subset=["item_id"])  # 去重，确保每个商品只出现一次
    
    result = (   #result 是一个 DataFrame，包含指定类别中销量最高的前 limit 个商品的信息，包括 item_id、title、price、sales、shop、province、style、fabric 和 fit 等列。数据按照销量降序排列，并重置索引。
        temp_df.sort_values("sales", ascending=False)
        .head(limit)[
            ["item_id", "title", "price", "sales", "shop", "province", "style", "fabric", "fit"]
        ]
        .reset_index(drop=True)
    )
    return result


def top_products_for_top_categories(df, category_limit=10, product_limit=10):
    """ 
        top_products_for_top_categories 函数首先调用 category_sales_analysis 函数获取类别销售数据，
        并选取销量最高的前 category_limit 个类别。然后，函数遍历这些类别，调用 top_products_by_category 
        函数获取每个类别中销量最高的前 product_limit 个商品，并将结果存储在 result 字典中，键为类别名称，
        值为对应的商品列表。具体来说，函数首先调用 category_sales_analysis(df) 获取类别销售数据，并使用 
        head(category_limit) 方法选取销量最高的前 category_limit 个类别。接着，函数初始化一个空字典 result，
        用于存储每个类别的 top products。然后，函数使用 for 循环遍历 category_sales_df 中的每个类别名称
        （category_name），在循环体内调用 top_products_by_category 函数，传入原始数据 df、当前类别名称 
        category_name 和商品数量限制 product_limit，获取该类别中销量最高的前 product_limit 个商品，
        并将结果转换为字典格式（使用 to_dict(orient="records")）后存储在 result 字典中，键为类别名称，
        值为对应的商品列表。最后，函数返回 result 字典，其中包含了每个类别的 top products 信息。"
    """
    category_sales_df = category_sales_analysis(df).head(category_limit)

    result = {}
    for category_name in category_sales_df["category"]:   # 遍历前 category_limit 个类别，调用 top_products_by_category 函数获取每个类别中销量最高的前 product_limit 个商品，并将结果存储在 result 字典中，键为类别名称，值为对应的商品列表。
        result[category_name] = top_products_by_category(
            df,
            category_name=category_name,
            limit=product_limit
        ).to_dict(orient="records")

    return result
#------------------------------------------------------------------------------------------------


def run_all_analysis(df):
    return {
        "category_sales": category_sales_analysis(df),  # 调用类别销售分析函数
        "province_sales": province_sales_analysis(df),
        "shop_sales": shop_sales_analysis(df),
        "style_price": style_price_analysis(df),
        "pattern_price": pattern_price_analysis(df),
        "fabric_price": fabric_price_analysis(df),
        "fit_price": fit_price_analysis(df),
    }
