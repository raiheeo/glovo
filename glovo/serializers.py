from rest_framework import serializers
from .models import *
from .models import Cart, CartItem


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
        fields = ['product_name', 'price', 'images', ]

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'images', 'description', 'quantity', "combo_products"]

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['status', 'client', 'products', 'delivery_address']

class OrderDetailSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ['status', 'client', 'products', 'delivery_address', 'courier', 'order_number', 'created_at']

class ComboListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['combo_name', 'combo_product', 'combo_image', 'discount']

class CourierSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['first_name', 'status']

class CourierDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['user', 'status', 'current_orders']

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['client', 'store', 'store_rating', 'comment', 'review_image']

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['client', 'store', 'store_rating', 'comment', 'review_image', 'courier', 'courier_rating']

class ReviewCourierSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['client', 'courier', 'courier_rating']

class ContactUsListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'