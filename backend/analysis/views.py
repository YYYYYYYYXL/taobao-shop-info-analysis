from pathlib import Path

import pandas as pd
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from src.analyze_data import run_all_analysis

from src.analyze_data import top_products_for_top_categories

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "cleaned_data.csv"
RESULT_LIMITS = {
    "category_sales": 10,
    "province_sales": 10,
    "shop_sales": 20,
    "style_price": 15,
    "pattern_price": 15,
    "fabric_price": 15,
    "fit_price": 10,
}


def api_response(data=None, code="0", msg="success", status=200):
    """ 
        统一响应封装函数。作用是把所有接口都包装成同一种格式：
        {
            "code": "0",
            "msg": "success",
            "data": ...
        }
        这样前端拿数据时结构统一，不用每个接口单独适配。
    """
    return JsonResponse(
        {
            "code": code, 
            "msg": msg, 
            "data": data
        },
        json_dumps_params={"ensure_ascii": False},
        status=status,
    )


@require_GET
def api_index(request):
    """ 
        作用是访问根路径时返回一个说明信息，告诉你：
        后端服务正在运行
        当前有哪些分析接口可用
        也就是你现在打开 127.0.0.1:8000/ 能看到的那个 JSON。
    """
    return api_response(
        msg="taobao analysis backend is running",
        data={
            "service": "taobao-analysis-backend",
            "endpoints": [
                "/api/category-sales/",
                "/api/analysis/province-sales",
                "/api/analysis/shop-sales",
                "/api/analysis/style-price",
                "/api/analysis/pattern-price",
                "/api/analysis/fabric-price",
                "/api/analysis/fit-price",
            ],
        },
    )


@require_GET
def favicon(request):
    """
        只是为了处理浏览器自动请求 /favicon.ico，避免 404。
        204 表示“请求成功，但没有内容”。
    """
    return JsonResponse({}, status=204)


def load_analysis_results():
    """ 
        读取 cleaned_data.csv
        调用 run_all_analysis(df)
        返回一整套分析结果
        这里返回的不是 JSON，而是一个字典，里面每个值还是 DataFrame
    """
    df = pd.read_csv(DATA_FILE)
    return run_all_analysis(df)


def build_chart_payload(result_key):
    results = load_analysis_results()
    raw_data = results[result_key].head(RESULT_LIMITS[result_key]).copy()
    value_column = raw_data.columns[-1]
    raw_data = raw_data.rename(columns={raw_data.columns[0]: "name", value_column: "value"})
    return raw_data[["name", "value"]].to_dict(orient="records")


@require_GET
def category_sales(request):
    return api_response(data=build_chart_payload("category_sales"))


@require_GET
def analysis_province_sales(request):
    return api_response(data=build_chart_payload("province_sales"))


@require_GET
def analysis_shop_sales(request):
    return api_response(data=build_chart_payload("shop_sales"))


@require_GET
def analysis_style_price(request):
    return api_response(data=build_chart_payload("style_price"))


@require_GET
def analysis_pattern_price(request):
    return api_response(data=build_chart_payload("pattern_price"))


@require_GET
def analysis_fabric_price(request):
    return api_response(data=build_chart_payload("fabric_price"))


@require_GET
def analysis_fit_price(request):
    return api_response(data=build_chart_payload("fit_price"))

@require_GET
def analysis_top_products_by_categories(request):
    df = pd.read_csv(DATA_FILE, skipinitialspace=True)
    data = top_products_for_top_categories(df, category_limit=10, product_limit=10)
    return api_response(data=data)
