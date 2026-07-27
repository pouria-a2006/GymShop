from django.shortcuts import get_object_or_404

from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from shop.models import ProductReview

from django_filters.rest_framework import DjangoFilterBackend

from shop.models import (
    Category,
    Brand,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Wishlist,
)

from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    RegisterSerializer,
    UserSerializer,
    LogoutSerializer,
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    WishlistSerializer,
    AddWishlistSerializer,
    ProductReviewSerializer,
    CreateReviewSerializer,

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

class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(
            Cart,
            user=request.user,
        )

        if not cart.items.exists():
            return Response(
                {"detail": "Cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = Order.objects.create(
            user=request.user,
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discount_price or item.product.price,
            )

        cart.items.all().delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )

class OrderListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

class OrderDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        )

class WishlistAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddWishlistSerializer

    def get(self, request):
        wishlist = Wishlist.objects.filter(
            user=request.user
        )

        serializer = WishlistSerializer(
            wishlist,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(
            Product,
            id=serializer.validated_data["product_id"],
        )

        Wishlist.objects.get_or_create(
            user=request.user,
            product=product,
        )

        return Response(
            {
                "detail": "Product added to wishlist."
            },
            status=status.HTTP_201_CREATED,
        )


class WishlistItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        item = get_object_or_404(
            Wishlist,
            id=pk,
            user=request.user,
        )

        item.delete()

        return Response(
            {
                "detail": "Removed from wishlist."
            },
            status=status.HTTP_200_OK,
        )

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductReview.objects.filter(
            product_id=self.kwargs["product_id"]
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateReviewSerializer
        return ProductReviewSerializer

    def perform_create(self, serializer):
        product = get_object_or_404(
            Product,
            id=self.kwargs["product_id"],
        )

        serializer.save(
            user=self.request.user,
            product=product,
        )


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return ProductReview.objects.filter(
            user=self.request.user
        )