from django.urls import path

from .views import CartAPIView, AddCartItemAPIView, ApplyCouponAPIView



urlpatterns = [
    path('', CartAPIView.as_view(), name='cart'),
    path('add/<int:pk>/', AddCartItemAPIView.as_view(), name='add_cart_item'),
    path('coupon/apply/', ApplyCouponAPIView.as_view(), name='apply'),

]