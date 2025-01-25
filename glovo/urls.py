from .views import *
from django.urls import path, include
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'user', UserViewSet, basename='user')
router.register(r'contact-us', ContactUsListView, basename='contact-us')


urlpatterns = [
    path('', include(router.urls)),
    path('user-profile/<int:pk>/', UserDetailViewSet.as_view(), name='user-profile'),
    path('cart/add-item/', CartViewSet.as_view({'post': 'add_item'}), name='cart-add-item'),
    path('cart/remove-item/', CartViewSet.as_view({'post': 'remove_item'}), name='cart-remove-item'),
    path('cart/clear/', CartViewSet.as_view({'post': 'clear'}), name='cart-clear'),
    #Store
    path('store/', StoreListAPIView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreOwnerEditAPIView.as_view(), name='store-edit'),
    path('store/list/', StoreOwnerListAPIView.as_view(), name='store-list-owner'),
    path('store/create/', StoreCreateAPIView.as_view(), name='store-create'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store-detail'),
    path('store/owner/', StoreOwnerListAPIView.as_view(), name='store-owner-list'),
    path('store/owner/edit/<int:pk>/', StoreOwnerEditAPIView.as_view(), name='store-owner-edit'),
    # Product
    path('product/', ProductListAPIView.as_view(), name='product-list'),
    path('product/owner/', ProductOwnerAPIView.as_view(), name='product-owner-list'),
    path('product/owner/edit/<int:pk>/', ProductOwnerEditAPIView.as_view(), name='product-owner-edit'),
    # Review
    path('review/', ReviewListAPIView.as_view(), name='review-list'),
    path('review/create/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('review/edit/<int:pk>/', ReviewEditCreateAPIView.as_view(), name='review-edit'),
    # Contact Us
    path('contact-us/create/', ContactUsCreateAPIView.as_view(), name='contact-us-create'),
    path('contact-us/edit/<int:pk>/', ContactUsEditCreateAPIView.as_view(), name='contact-us-edit'),
    # Discount
    path('discount/', DiscountListAPIView.as_view(), name='discount-list'),
    path('discount/<int:pk>/', DiscountDetailAPIView.as_view(), name='discount-detail'),
    path('discount/create/', DiscountCreateAPIView.as_view(), name='discount-create'),
    path('discount/owner/', DiscountOwnerListAPIView.as_view(), name='discount-owner-list'),
    path('discount/owner/edit/<int:pk>/', DiscountOwnerEditAPIView.as_view(), name='discount-owner-edit'),
    # Combo
    path('combo/', ComboListAPIView.as_view(), name='combo-list'),
    path('combo/detail/<int:pk>/', ComboDetailAPIView.as_view(), name='combo-detail'),
    # Courier
    path('courier/review/', CourierReviewAPIView.as_view(), name='courier-review'),
    path('courier/', CourierListAPIView.as_view(), name='courier-list'),
    path('courier/detail/<int:pk>/', CourierDetailAPIView.as_view(), name='courier-detail'),
    # Category
    path('category/', CategoryAPIView.as_view(), name='category-list'),
    # Order
    path('order/', OrderListAPIView.as_view(), name='order-list'),
    path('order/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('order/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('order/owner/edit/<int:pk>/', OrderOwnerEditAPIView.as_view(), name='order-owner-edit'),
]

#all urls from views


