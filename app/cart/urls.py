from django.urls import path

from .views import CartAPIView, AddCartItemAPIView



urlpatterns = [
    path('', CartAPIView.as_view(), name='cart'),
    path('add/<int:pk>/', AddCartItemAPIView.as_view(), name='add_cart_item'),

]