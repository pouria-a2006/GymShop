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

    list_display = (
        "name",
        "category",
        "brand",
        "price",
        "discount_price",
        "stock",
        "image_count",
        "attribute_count",
        "inventory_count",
        "is_available",
    )

    list_filter = (
        "category",
        "brand",
        "is_available",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "brand__name",
        "category__name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    ordering = ("-created_at",)

    list_per_page = 20

    fieldsets = (
        ("Product Information", {
            "fields": (
                "name",
                "slug",
                "category",
                "brand",
                "description",
            )
        }),
        ("Pricing", {
            "fields": (
                "price",
                "discount_price",
            )
        }),
        ("Inventory", {
            "fields": (
                "stock",
                "weight",
                "is_available",
            )
        }),
        ("Media", {
            "fields": (
                "image",
            )
        }),
    )

    @admin.action(description="Mark selected products as available")
    def make_available(self, request, queryset):
        queryset.update(is_available=True)

    @admin.action(description="Mark selected products as unavailable")
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    @admin.action(description="Reset stock to zero")
    def reset_stock(self, request, queryset):
        queryset.update(stock=0)

    def image_count(self, obj):
        return obj.gallery.count()
    image_count.short_description = "Images"


    def attribute_count(self, obj):
        return obj.attributes.count()
    attribute_count.short_description = "Attributes"


    def inventory_count(self, obj):
        return obj.inventory.count()
    inventory_count.short_description = "Inventory"

    
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