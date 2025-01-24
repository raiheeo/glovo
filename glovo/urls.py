from .views import *
from django.urls import path, include
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'cart', CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls)),
    path('store/', StoreListAPIView.as_view(), name='hotel_list'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='hotel_detail'),
]