from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
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