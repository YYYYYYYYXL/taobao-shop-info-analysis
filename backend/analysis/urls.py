from django.urls import path

from .views import (
    analysis_fabric_price,
    analysis_fit_price,
    analysis_pattern_price,
    analysis_province_sales,
    analysis_shop_sales,
    analysis_style_price,
    category_sales,
)


urlpatterns = [
    path("category-sales/", category_sales),
    path("analysis/province-sales", analysis_province_sales),
    path("analysis/shop-sales", analysis_shop_sales),
    path("analysis/style-price", analysis_style_price),
    path("analysis/pattern-price", analysis_pattern_price),
    path("analysis/fabric-price", analysis_fabric_price),
    path("analysis/fit-price", analysis_fit_price),
]
