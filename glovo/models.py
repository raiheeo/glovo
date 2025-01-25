from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum
from django.db import transaction
from datetime import datetime, timedelta
from django.conf import settings


class Category(models.Model):
    category_name = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.category_name


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True, region='KZ', default='+7')
    age = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(18), MaxValueValidator(75)], null=True, blank=False)
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('owner', 'Owner'),
        ('admin', 'Admin'),
    )
    status = models.CharField(max_length=32, choices=ROLE_CHOICES, default='client')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class Store(models.Model):
    owner = models.ForeignKey('glovo.UserProfile', on_delete=models.CASCADE, null=True, blank=True)
    store_name = models.CharField(max_length=128, verbose_name='Store/Name', null=True, blank=True)
    store_description = models.TextField(verbose_name='Store/Description', null=True, blank=True)
    contact_email = models.EmailField()
    contact_phone = PhoneNumberField(null=True, blank=True, region='KG')
    address = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return f' {self.store_name}, {self.address}'

class Discount(models.Model):
    name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=20, choices=[
        ('percent', 'Percentage Discount'),
        ('fixed', 'Fixed Discount'),
    ], default='percent')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True,)

    def is_active(self):
        now = timezone.now()
        return self.active and (self.start_date is None or self.start_date <= now) and (
                    self.end_date is None or self.end_date >= now)

    def __str__(self):
        return f"{self.name} ({self.value} {'%' if self.discount_type == 'percent' else 'currency'})"


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_store')
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL, related_name="product_orders")
    product_name = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 100)],)
    combo = models.ForeignKey('Combo', null=True, blank=True, on_delete=models.CASCADE, related_name="combo_products")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, related_name='product_category')

    def old_price(self):
        return self.price

    def new_price(self):
        if self.discount and self.discount.is_active():
            if self.discount.discount_type == 'percent':
                return self.price * (1 - self.discount.value / 100)
            elif self.discount.discount_type == 'fixed':
                return max(0, self.price - self.discount.value)
        return self.price

    def __str__(self):
        return f'{self.product_name} and {self.price}'

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    client = models.ForeignKey('glovo.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    products = models.ManyToManyField(Product, related_name="product_orders")
    delivery_address = models.TextField()
    courier = models.ForeignKey('Courier', on_delete=models.SET_NULL, null=True, blank=True, related_name='courier_deliveries')
    created_at = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=20, unique=True)
    items = models.ManyToManyField('CartItem')

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def old_total_price(self):
        return sum(product.old_price() for product in self.products.all())

    def new_total_price(self):
        total = sum(product.new_price() for product in self.products.all())
        if self.discount and self.discount.is_active():
            if self.discount.discount_type == 'percent':
                total *= (1 - self.discount.value / 100)
            elif self.discount.discount_type == 'fixed':
                total = max(0, total - self.discount.value)
        return total

    def __str__(self):
        return f'Order #{self.id} for {self.user}'


class Combo(models.Model):
    combo_name = models.CharField(max_length=64, null=True, blank=True)
    combo_product = models.ManyToManyField(Product, related_name='combo_product')
    is_combo = models.BooleanField(null=True, blank=True)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL, related_name="combos")
    combo_image = models.ForeignKey('ComboImage', null=True, blank=True, on_delete=models.SET_NULL, related_name="images_combo")

    def old_total_price(self):
        return sum(product.old_price() for product in self.products.all())

    def new_total_price(self):
        total = sum(product.new_price() for product in self.products.all())
        if self.discount and self.discount.is_active():
            if self.discount.discount_type == 'percent':
                total *= (1 - self.discount.value / 100)
            elif self.discount.discount_type == 'fixed':
                total = max(0, total - self.discount.value)
        return total

    def __str__(self):
        return f"{self.name} (Discount: {self.discount.value} {'%' if self.discount.discount_type == 'percent' else 'currency'})"

class Courier(models.Model):
     user = models.ForeignKey('glovo.UserProfile', on_delete=models.CASCADE, related_name='courier_user')
     STATUS_CHOICES = [
         ('busy', 'Busy'),
         ('free', 'Free'),
     ]
     status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='free')
     current_orders = models.ManyToManyField('Order', blank=True, related_name='couriers')

     def __str__(self):
         return {self.user}


class Review(models.Model):
    client = models.ForeignKey('glovo.UserProfile', on_delete=models.CASCADE, related_name='review_user')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='review_store')
    store_rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)],)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name='review_courier')
    courier_rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)],)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)],)
    comment = models.CharField(max_length=256, null=True, blank=True)
    review_image = models.ImageField(upload_to='review_image/')

    def __str__(self):
        return f'{self.store},{self.courier},{self.rating}'

class ComboImage(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, related_name='combo_images')
    combo_image = models.ImageField(upload_to='combo_images/')

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    product_image = models.ImageField(upload_to='product_image/')

class ContactUs(models.Model):
    username = models.ForeignKey('glovo.UserProfile', on_delete=models.CASCADE, related_name='user_contact')
    issue = models.CharField(max_length=256, blank=True, null=True)
    gmail = models.EmailField()
    contact_date = models.DateTimeField(auto_now_add=True)
    phonenumber_field = PhoneNumberField(region='KZ',null=True, blank=False, default='+7')

    def __str__(self):
        return self.contact_date.strftime('%Y-%m-%d %H:%M:%S')


class Cart(models.Model):
    cart_user = models.OneToOneField('glovo.UserProfile', on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'{self.cart_user}'

    def add_item(self, product, quantity=1):
        item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            item.quantity += quantity
            item.save()
        return item

    def remove_item(self, product):
        CartItem.objects.filter(cart=self, product=product).delete()

    def get_total_price(self):
        return self.items.aggregate(total=Sum('product__price'))['total'] or 0

    def create_order(self):
        with transaction.atomic():
            order = Order.objects.create(user=self.cart_user)
            for item in self.items.all():
                order.items.add(item)
            order.save()
            self.items.all().delete()
        return order


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} (x{self.quantity})'




