from django.conf import settings
from django.db import models
from django.utils import timezone

from movies.models import MoviesModel


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'در انتظار پرداخت'
        SUCCESS = 'success', 'موفق'
        FAILED = 'failed', 'ناموفق'
        EXPIRED = 'expired', 'منقضی شده'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='payments')
    subscription_plan = models.ForeignKey('accounts.SubscriptionPlan',on_delete=models.PROTECT,null=True,blank=True,related_name='payments')
    amount = models.PositiveBigIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    authority = models.CharField(max_length=255, null=True, blank=True, unique=True)
    reference_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.PROTECT, null=True, blank=True, related_name='payments', verbose_name='کد تخفیف')
    discount_amount = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ تخفیف')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Payment #{self.user.username}'

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'


class PaymentItem(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name='items')
    movie = models.ForeignKey(MoviesModel, on_delete=models.PROTECT)
    price = models.PositiveBigIntegerField()

    class Meta:
        verbose_name = 'آیتم پرداخت'
        verbose_name_plural = 'آیتم های پرداخت'

        constraints = [
            models.UniqueConstraint(
                fields=['payment', 'movie'],
                name='unique_movie_per_payment',
            )
        ]

    def __str__(self):
        return f'{self.payment.user.username} - {self.movie.title}'


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='کد تخفیف')
    discount = models.PositiveSmallIntegerField(verbose_name='درصد تخفیف')
    max_uses = models.PositiveIntegerField(default=1, verbose_name='حداکثر استفاده')
    used_count = models.PositiveIntegerField(default=0, verbose_name='تعداد استفاده')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    valid_from = models.DateTimeField(null=True, blank=True, verbose_name='شروع اعتبار')
    valid_until = models.DateTimeField(null=True, blank=True, verbose_name='پایان اعتبار')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.code

    @property
    def is_valid(self):
        now = timezone.now()

        if not self.is_active:
            return False

        if self.used_count >= self.max_uses:
            return False

        if self.valid_from and now < self.valid_from:
            return False

        if self.valid_until and now > self.valid_until:
            return False

        return True

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'


class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE,related_name='usages',verbose_name='کد تخفیف')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='coupon_usages',verbose_name='کاربر')
    used_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ استفاده')

    class Meta:
        verbose_name = 'استفاده از کد تخفیف'
        verbose_name_plural = 'استفاده‌های کد تخفیف'
        constraints = [
            models.UniqueConstraint(
                fields=['coupon', 'user'],
                name='unique_coupon_usage_per_user',
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.coupon.code}'