from django.urls import path

from .views import (
    CategoryListAPIView,
    BrandListAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    RegisterAPIView,
    ProfileAPIView,
    LogoutAPIView,
    CartAPIView,
    CartItemAPIView,
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

    path(
    "register/",
    RegisterAPIView.as_view(),
    name="api-register",
    ),

    path(
    "profile/",
    ProfileAPIView.as_view(),
    name="api-profile",
    ),

    path(
    "logout/",
    LogoutAPIView.as_view(),
    name="api-logout",
    ),

    path(
    "cart/",
    CartAPIView.as_view(),
    name="api-cart",
    ),

    path(
    "cart/items/<int:pk>/",
    CartItemAPIView.as_view(),
    name="api-cart-item",
    ),
]