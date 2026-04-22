from pathlib import Path

import pandas as pd
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from src.analyze_data import (
    dataframe_to_records,
    run_all_analysis,
    top_products_by_dimension,
    top_products_for_top_categories,
)

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
DETAIL_FIELD_MAP = {
    "category": "category",
    "province": "province",
    "shop": "shop",
    "style": "style",
    "pattern": "pattern",
    "fabric": "fabric",
    "fit": "fit",
}


def api_response(data=None, code="0", msg="success", status=200):
    return JsonResponse(
        {
            "code": code,
            "msg": msg,
            "data": data,
        },
        json_dumps_params={"ensure_ascii": False},
        status=status,
    )


@require_GET
def api_index(request):
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
                "/api/analysis/top-products-by-categories",
                "/api/analysis/top-products-by-dimension?field=category&value=外套",
            ],
        },
    )


@require_GET
def favicon(request):
    return JsonResponse({}, status=204)


def load_analysis_results():
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


@require_GET
def analysis_top_products_by_dimension(request):
    field = request.GET.get("field", "").strip()
    value = request.GET.get("value", "").strip()

    if field not in DETAIL_FIELD_MAP:
        return api_response(code="1", msg="unsupported field", data=[], status=400)

    if not value:
        return api_response(code="1", msg="missing value", data=[], status=400)

    df = pd.read_csv(DATA_FILE, skipinitialspace=True)
    detail_df = top_products_by_dimension(
        df,
        field=DETAIL_FIELD_MAP[field],
        value=value,
        limit=10,
    )
    return api_response(data=dataframe_to_records(detail_df))
