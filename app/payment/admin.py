from django.contrib import admin

from .models import  Payment, PaymentItem, Coupon, CouponUsage


admin.site.register(Payment)
admin.site.register(PaymentItem)
admin.site.register(Coupon)
admin.site.register(CouponUsage)
