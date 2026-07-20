from django.contrib import admin
from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
    Inventory,
    ProductAttribute,
    ProductReview,
)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    inlines = [
        ProductImageInline,
        InventoryInline,
        ProductAttributeInline,
    ]

    actions = [
        "make_available",
        "make_unavailable",
        "reset_stock",
    ]

    ...

    ordering = ("-created_at",)

    @admin.action(description="Mark selected products as available")
    def make_available(self, request, queryset):
        queryset.update(is_available=True)

    @admin.action(description="Mark selected products as unavailable")
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    @admin.action(description="Reset stock to zero")
    def reset_stock(self, request, queryset):
        queryset.update(stock=0)
   
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "created_at",
    )

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "sku",
        "quantity",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "product__name",
        "sku",
    )

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "name",
        "value",
    )

    search_fields = (
        "product__name",
        "name",
        "value",
    )

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "name",
        "rating",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_approved",
    )

    search_fields = (
        "product__name",
        "name",
        "email",
    )