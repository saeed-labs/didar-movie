from django.urls import path

from .views import (
    PaymentRequestAPIView,
    ZarinpalCallbackAPIView,
)

app_name = "payments"

urlpatterns = [
    path("request/", PaymentRequestAPIView.as_view(), name="request"),

    path("zarinpal/callback/", ZarinpalCallbackAPIView.as_view(), name="zarinpal-callback"),
]
