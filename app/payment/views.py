from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart

from utils.gateways.zarinpal import ZarinpalGateway
from utils.gateways.services import complete_payment

from .models import Payment, PaymentItem, MovieOwnership


class PaymentRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        cart = get_object_or_404(Cart.objects.select_for_update(),user=request.user,)

        cart_items = list(cart.items.select_related("movie"))

        if not cart_items:
            return Response(
                {"detail": "سبد خرید خالی است."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        owned_movie_ids = set(
            MovieOwnership.objects.filter(
                user=request.user,
                movie_id__in=[
                    item.movie_id
                    for item in cart_items
                ],
            ).values_list(
                "movie_id",
                flat=True,
            )
        )

        cart_items = [item for item in cart_items if item.movie_id not in owned_movie_ids]

        if not cart_items:
            return Response(
                {
                    "detail": "تمام فیلم‌های سبد خرید قبلاً خریداری شده‌اند."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_price = sum(item.movie.price for item in cart_items)

        payment = Payment.objects.create(
            user=request.user,
            amount=total_price,
            status=Payment.Status.PENDING,
        )

        PaymentItem.objects.bulk_create([
            PaymentItem(
                payment=payment,
                movie=item.movie,
                price=item.movie.price,
            )
            for item in cart_items
        ])

        callback_url = request.build_absolute_uri(reverse("payments:zarinpal-callback"))

        gateway = ZarinpalGateway()

        result = gateway.request_payment(
            amount=payment.amount,
            description=f"خرید فیلم - Payment #{payment.id}",
            callback_url=callback_url,
            mobile=request.user.phone,
            email=request.user.email,
        )

        data = result.get("data", {})

        if data.get("code") != 100:
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])

            return Response(
                {
                    "detail": "ایجاد پرداخت در زرین‌پال ناموفق بود.",
                    "code": data.get("code"),
                    "message": data.get("message"),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        authority = data["authority"]

        payment.authority = authority

        payment.save(update_fields=["authority"])

        return Response(
            {
                "payment_id": payment.id,
                "amount": payment.amount,
                "authority": authority,
                "payment_url": gateway.get_payment_url(authority),
            },
            status=status.HTTP_201_CREATED,
        )



class ZarinpalCallbackAPIView(APIView):

    def get(self, request):

        authority = request.GET.get("Authority")
        status_value = request.GET.get("Status")

        if not authority:
            return Response(
                {"detail": "Authority ارسال نشده است."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if status_value != "OK":
            return Response(
                {"detail": "پرداخت توسط کاربر لغو یا ناموفق شد."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = get_object_or_404(
            Payment,
            authority=authority,
        )

        if payment.status == Payment.Status.SUCCESS:
            return Response(
                {
                    "detail": "این پرداخت قبلاً تایید شده است."
                }
            )

        gateway = ZarinpalGateway()

        result = gateway.verify_payment(
            amount=payment.amount,
            authority=authority,
        )

        data = result.get("data", {})

        code = data.get("code")

        if code not in [100, 101]:
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])

            return Response(
                {
                    "detail": "پرداخت تایید نشد.",
                    "code": code,
                    "message": data.get("message"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        reference_id = data.get("ref_id")

        complete_payment(
            payment=payment,
            reference_id=reference_id,
        )

        return Response(
            {
                "detail": "پرداخت با موفقیت انجام شد.",
                "payment_id": payment.id,
                "reference_id": reference_id,
            }
        )