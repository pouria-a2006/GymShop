from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Wishlist
from django.utils.html import format_html
from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
    Inventory,
    ProductAttribute,
    ProductReview,
)



@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "rating",
        "is_approved",
        "created_at",
    )

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
        "stock_status",
        "availability_status",
        "created_at",
        "updated_at",
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

    ordering = ("-created_at",)

    list_per_page = 20
  
    readonly_fields = (
        "created_at",
        "updated_at",
        "image_preview",
    )

    fieldsets = (
        ("Product Information", {
            "fields": (
                "name",
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
                "image_preview",
            )
        }),
        ("Dates", {
            "fields": (
                "created_at",
                "updated_at",
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


    def stock_status(self, obj):
        if obj.stock == 0:
            return mark_safe(
                '<span style="color:red;"><b>Out of Stock</b></span>'
            )

        elif obj.stock < 10:
            return mark_safe(
                '<span style="color:orange;"><b>Low Stock</b></span>'
            )

        return mark_safe(
            '<span style="color:green;"><b>In Stock</b></span>'
        )

    stock_status.short_description = "Stock Status"

    def availability_status(self, obj):
        if obj.is_available:
            return mark_safe(
                '<span style="color:green;"><b>Available</b></span>'
            )

        return mark_safe(
            '<span style="color:red;"><b>Unavailable</b></span>'
        )

    availability_status.short_description = "Availability"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="120" style="border-radius:10px;" />',
                obj.image.url
            )

        return "No Image"

    image_preview.short_description = "Preview"


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



@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "created_at",
    )

    search_fields = (
        "user__username",
        "product__name",
    )