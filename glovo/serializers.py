from rest_framework import serializers
from .models import *
import datetime
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'phone_number', 'age')


class ComboImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboImage
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'cart_user', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.items.all())


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']

class UserSimpleSerializer(serializers.Serializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'phone_number', 'registered_at', 'status']

class StoreListSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    class Meta:
        model = Store
        fields = ['store_name', 'address']

class StoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_name', 'store_description', 'contact_email', 'contact_phone', 'address']

class DiscountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['name', 'value', 'active']

class DiscountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['name', 'value', 'active', 'start_date', 'end_date', 'is_active']

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'price']

class ProductDetailSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'images', 'description', 'quantity', "combo_products", 'product_image']

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'client', 'products', 'delivery_address']

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'client', 'products', 'delivery_address', 'courier', 'order_number', 'created_at']

class ComboListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = ['combo_name', 'combo_product', 'combo_image', 'discount']

class ComboDetailSerializer(serializers.ModelSerializer):
    combo_image = ComboImageSerializer(many=True, read_only=True)
    class Meta:
        model = Combo
        fields = ['combo_name', 'combo_product', 'combo_image', 'discount', 'combo_image']

class CourierSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ['status']

class CourierDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ['user', 'status', 'current_orders']

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['client', 'store', 'store_rating', 'comment', 'review_image']

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['client', 'store', 'store_rating', 'comment', 'review_image', 'courier', 'courier_rating']

    def get_created_date(self, obj):
        created_date = obj.created_date
        if isinstance(created_date, datetime.datetime):
            created_date = created_date.date()
        return created_date.strftime('%d-%m-%Y') if created_date else None


class ReviewCourierSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['client', 'courier', 'courier_rating']


class ContactUsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
