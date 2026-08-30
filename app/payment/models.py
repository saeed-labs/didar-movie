from django.conf import settings
from django.db import models

from accounts.models import User
from movies.models import MoviesModel


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'در انتظار پرداخت'
        SUCCESS = 'success', 'موفق'
        FAILED = 'failed', 'ناموفق'
        EXPIRED = 'expired', 'منقضی شده'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='payments')
    amount = models.PositiveBigIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    authority = models.CharField(max_length=255, null=True, blank=True, unique=True)
    reference_id = models.CharField(max_length=255, null=True, blank=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Payment #{self.user.username}'


class PaymentItem(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name='items')
    movie = models.ForeignKey(MoviesModel, on_delete=models.PROTECT)
    price = models.PositiveBigIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['payment', 'movie'],
                name='unique_movie_per_payment',
            )
        ]

    def __str__(self):
        return f'{self.payment.user.username} - {self.movie.title}'

class MovieOwnership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='movie_ownerships')
    movie = models.ForeignKey(MoviesModel, on_delete=models.PROTECT, related_name='owners')
    payment = models.ForeignKey('Payment', on_delete=models.PROTECT, related_name='ownerships')
    price = models.PositiveBigIntegerField()
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'],
                name='unique_user_movie_ownership',
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.movie}'
