from django.urls import path

from .views import (
    CategoryListAPIView,
    BrandListAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
)

urlpatterns = [
    path(
        "categories/",
        CategoryListAPIView.as_view(),
        name="api-categories",
    ),

    path(
        "brands/",
        BrandListAPIView.as_view(),
        name="api-brands",
    ),

    path(
        "products/",
        ProductListAPIView.as_view(),
        name="api-products",
    ),

    path(
        "products/<int:pk>/",
        ProductDetailAPIView.as_view(),
        name="api-product-detail",
    ),
]