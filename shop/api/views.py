from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import UpdateCartItemSerializer
from shop.models import (
    Category,
    Brand,
    Product,
)

from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    RegisterSerializer,
    UserSerializer,
    LogoutSerializer,
)
from rest_framework.views import APIView

from shop.models import Cart

from .serializers import (
    CartSerializer,
)

from django.shortcuts import get_object_or_404
from shop.models import Cart, CartItem, Product
from .serializers import AddToCartSerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    search_fields = [
        "name",
        "description",
        "brand__name",
        "category__name",
    ]

    filterset_fields = [
        "category",
        "brand",
        "is_available",
    ]

    ordering_fields = [
        "price",
        "stock",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_205_RESET_CONTENT,
        )

class CartAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(
            Product,
            id=serializer.validated_data["product_id"],
        )

        quantity = serializer.validated_data["quantity"]

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK,
        )

class CartItemAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCartItemSerializer

    def patch(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)

        item = get_object_or_404(
            CartItem,
            id=pk,
            cart=cart,
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item.quantity = serializer.validated_data["quantity"]
        item.save()

        return Response(
            CartSerializer(cart).data
        )

    def delete(self, request, pk):
        cart = get_object_or_404(
            Cart,
            user=request.user,
        )

        item = get_object_or_404(
            CartItem,
            id=pk,
            cart=cart,
        )

        item.delete()

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK,
        )