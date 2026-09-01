from django.conf import settings
from django.db import models

from movies.models import MoviesModel
from payment.models import Coupon


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart',verbose_name='کاربر', )
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='carts', verbose_name='کد تخفیف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی', )

    def __str__(self):
        return f'سبد خرید {self.user.username}'

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید', )
    movie = models.ForeignKey(MoviesModel, on_delete=models.CASCADE, related_name='cart_items', verbose_name='فیلم',)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ افزودن', )

    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'

        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'movie'],
                name='unique_movie_per_cart',
            )
        ]

    def __str__(self):
        return f'{self.cart.user.username} - {self.movie.title}'
