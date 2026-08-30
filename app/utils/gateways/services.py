from django.db import transaction
from django.utils import timezone

from payment.models import Payment, MovieOwnership
from cart.models import Cart

@transaction.atomic
def complete_payment(payment, reference_id):

    payment = (
        Payment.objects
        .select_for_update()
        .prefetch_related("items")
        .get(pk=payment.pk)
    )

    if payment.status == Payment.Status.SUCCESS:
        return

    payment.status = Payment.Status.SUCCESS
    payment.reference_id = reference_id
    payment.paid_at = timezone.now()

    payment.save(
        update_fields=[
            "status",
            "reference_id",
            "paid_at",
        ]
    )

    MovieOwnership.objects.bulk_create(
        [
            MovieOwnership(
                user=payment.user,
                movie=item.movie,
                payment=payment,
                price=item.price,
            )
            for item in payment.items.all()
        ],
        ignore_conflicts=True,
    )

    cart = Cart.objects.filter(
        user=payment.user
    ).first()

    if cart:
        movie_ids = payment.items.values_list("movie_id",flat=True)
        cart.items.filter(movie_id__in=movie_ids).delete()