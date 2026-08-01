from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from shop.models import Cart, CartItem
from shop.models import ProductReview

from shop.models import (
    Category,
    Brand,
    Product,
     Order,
    OrderItem,
    Wishlist,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
        ]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "slug",
        ]
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "discount_price",
            "stock",
            "weight",
            "is_available",
            "image",
            "category",
            "brand",
        ]     

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
        ]


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self, **kwargs):
        refresh_token = self.validated_data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "total_price",
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_price",
        ]

    def get_total_price(self, obj):
        return sum(item.total_price for item in obj.items.all())


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "quantity",
            "price",
            "total_price",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "created_at",
            "items",
        ]

class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = (
            "id",
            "product",
            "created_at",
        )


class AddWishlistSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProductReview
        fields = (
            "id",
            "user",
            "rating",
            "comment",
            "created_at",
        )


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = (
            "rating",
            "comment",
        )