from django.db import transaction
from django.utils import timezone
from django.db.models import F

from movies.models import MoviesModel
from payment.models import Payment, Coupon, CouponUsage
from accounts.models import MovieOwnership
from cart.models import Cart


@transaction.atomic
def complete_payment(payment, reference_id):
    payment = (Payment.objects.select_for_update().prefetch_related("items").get(pk=payment.pk))

    if payment.status == Payment.Status.SUCCESS:
        return

    payment.status = Payment.Status.SUCCESS
    payment.reference_id = reference_id
    payment.paid_at = timezone.now()

    payment.save(update_fields=["status", "reference_id", "paid_at"])



    # =========================
    # Movie Purchase
    # =========================
    items = list(payment.items.select_related("movie"))

    MovieOwnership.objects.bulk_create(
        [
            MovieOwnership(
                user=payment.user,
                movie=item.movie,
                payment=payment,
                price=item.price,
            )
            for item in items
        ],
        ignore_conflicts=True,
    )


    # =========================
    # Coupon
    # =========================
    if payment.coupon_id:
        coupon = (Coupon.objects.select_for_update().get(pk=payment.coupon_id))
        CouponUsage.objects.create(coupon=coupon, user=payment.user)
        coupon.used_count = coupon.used_count + 1
        coupon.save(update_fields=["used_count"])


    # =========================
    # Subscription
    # =========================
    if payment.subscription_plan_id:
        profile = payment.user.profile
        now = timezone.now()
        if (profile.is_special and profile.special_expires_at and profile.special_expires_at > now):
            start_date = profile.special_expires_at
        else:
            start_date = now
        profile.is_special = True
        profile.special_expires_at = (start_date + timezone.timedelta(days=payment.subscription_plan.duration_days))
        profile.save(update_fields=["is_special", "special_expires_at", ])



    # =========================
    # Cart
    # =========================
    for item in items:
        MoviesModel.objects.filter(pk=item.movie_id).update(beloved=F("beloved") + 1)

    cart = Cart.objects.filter(user=payment.user).first()

    if cart:
        movie_ids = payment.items.values_list("movie_id", flat=True)
        cart.items.filter(movie_id__in=movie_ids).delete()
        cart.coupon = None
        cart.save(update_fields=["coupon", "updated_at"])
