from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin
from django.conf import settings
from django.urls import reverse


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Product
    extra = 1

class ComboImageInLine(admin.TabularInline):
    model = ComboImage
    extra = 1

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    inlines = [ProductImageInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    readonly_fields = ('new_price_display',)

    def new_price_display(self, obj):
        if obj.new_price() is not None:
            return f"{obj.new_price():.2f}"
        return "N/A"

    new_price_display.short_description = 'Price after Discount'
    list_display = ('product_name', 'price', 'new_price_display',)


@admin.register(Store)
class StoreAdmin(TranslationAdmin):
    inlines = [ProductInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Combo)
class ComboAdmin(TranslationAdmin):
    inlines = [ComboImageInLine]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart_user')
    search_fields = ('cart_user__username',)
    list_filter = ('cart_user',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    search_fields = ('product__name', 'cart__cart_user__username')
    list_filter = ('cart', 'product')

admin.site.register(Courier)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Discount)
admin.site.register(ComboImage)
admin.site.register(ProductImage)
admin.site.register(ContactUs)



