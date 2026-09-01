from django.urls import path

from .views import (
    PaymentRequestAPIView,
    ZarinpalCallbackAPIView,
    SubscriptionPaymentRequestAPIView,
    SubscriptionPlanListAPIView
)

app_name = "payments"

urlpatterns = [
    path("request/", PaymentRequestAPIView.as_view(), name="request"),
    path("zarinpal/callback/", ZarinpalCallbackAPIView.as_view(), name="zarinpal-callback"),
    path("subscription/plans/", SubscriptionPlanListAPIView.as_view(), name="subscription-plans"),
    path("subscription/plans/<int:pk>/", SubscriptionPaymentRequestAPIView.as_view(), name="subscription"),
]
