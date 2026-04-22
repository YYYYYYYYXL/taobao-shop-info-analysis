from django.urls import path

from .views import (
    analysis_fabric_price,
    analysis_fit_price,
    analysis_pattern_price,
    analysis_province_sales,
    analysis_shop_sales,
    analysis_style_price,
    analysis_top_products_by_dimension,
    category_sales,
    analysis_top_products_by_categories,
)


urlpatterns = [
    path("category-sales/", category_sales),
    path("analysis/province-sales", analysis_province_sales),
    path("analysis/shop-sales", analysis_shop_sales),
    path("analysis/style-price", analysis_style_price),
    path("analysis/pattern-price", analysis_pattern_price),
    path("analysis/fabric-price", analysis_fabric_price),
    path("analysis/fit-price", analysis_fit_price),
    path("analysis/top-products-by-categories", analysis_top_products_by_categories),
    path("analysis/top-products-by-dimension", analysis_top_products_by_dimension),
]
