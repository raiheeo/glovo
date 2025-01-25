from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem, Product
from .serializers import  *
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import *
from .permissions import *



class CartViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        cart = get_object_or_404(Cart, cart_user=pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        cart = get_object_or_404(Cart, cart_user=pk)
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='remove-item')
    def remove_item(self, request, pk=None):
        cart = get_object_or_404(Cart, cart_user=pk)
        product_id = request.data.get('product')

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()

        return Response({"message": "Item removed successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='clear')
    def clear(self, request, pk=None):
        cart = get_object_or_404(Cart, cart_user=pk)
        cart.items.all().delete()
        return Response({"message": "Cart cleared successfully"}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        print(f"User: {self.request.user}, Action: {self.action}")
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAdmin | IsClient | IsCourier | CheckOwner]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsClient]
        elif self.action in ['clear']:
            permission_classes = [IsClient | IsAdmin]
        else:
            permission_classes = [IsAdmin]
        return [perm() for perm in permission_classes]


class UserViewSet(viewsets.ModelViewSet):
    queryset =  UserProfile.objects.all()
    serializer_class = UserSimpleSerializer

    def get_queryset(self):
         return UserProfile.objects.filter(id=self.request.user.id)

class UserDetailViewSet(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnProfile, IsAdmin]


class StoreListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['store_name', 'address']

class StoreDetailAPIView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer

class StoreCreateAPIView(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [CheckOwner, IsAdmin]

    def post(self, request, *args, **kwargs):
        return Response({"message": "Store created successfully"})


class StoreOwnerListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    permission_classes = [CheckOwner, IsAdmin]

    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)

class StoreOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [CheckOwner, CheckOwnerEdit, IsAdmin]

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['product_name']

class ProductOwnerAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [CheckOwner, IsAdmin]

    def get_queryset(self):
        user_instance = self.request.user
        return Product.objects.filter(hotel__owner=user_instance)

class ProductOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CheckOwner, CheckOwnerEdit, IsAdmin]

class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset =  Review.objects.all()
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsClient, IsAdmin]

class ReviewEditCreateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    permission_classes = [CheckAuthor, IsAdmin]

    def get_queryset(self):
        return Review.objects.all.filter(user=self.request.user)

class ContactUsListView(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializers_class = ContactUsListSerializer
    permission_classes = [CheckAuthor, IsAdmin, CheckOwner]

class ContactUsEditCreateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactDetailSerializer
    permission_classes = [IsAdmin]

class ContactUsCreateAPIView(generics.CreateAPIView):
    queryset =  ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdmin, IsClient]

class DiscountListAPIView(generics.ListAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = DiscountFilter
    search_fields = ['name', 'discount_type']

class DiscountDetailAPIView(generics.RetrieveAPIView):
    queryset = Discount.objects.all()
    serializers_class = DiscountDetailSerializer

class DiscountCreateAPIView(generics.CreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [CheckOwner, CheckOwnerEdit, IsAdmin]

class DiscountOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [CheckOwner, CheckOwnerEdit, IsAdmin]

class DiscountOwnerListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = DiscountListSerializer
    permission_classes = [CheckOwner, IsAdmin]

    def get_queryset(self):
        user_instance = self.request.user
        return Discount.objects.filter(store__owner=user_instance)

class ComboListAPIView(generics.ListAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboListSerializer

class ComboDetailAPIView(generics.ListAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboDetailSerializer

class CourierReviewAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCourierSerializer

class CourierListAPIView(generics.ListAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSimpleSerializer

class CourierDetailAPIView(generics.ListAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierDetailSerializer
    permission_classes = [IsCourier, IsOwnProfile, IsAdmin, CheckOwner]

class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CategoryFilter
    search_fields = ['category_name']

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializers_class = OrderListSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsOwnProfile, IsAdmin, IsCourier, CheckOwner]

class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CheckOwner, CheckOwnerEdit, IsAdmin]

