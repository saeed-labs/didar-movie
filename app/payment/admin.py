from django.contrib import admin

from .models import MovieOwnership, Payment, PaymentItem


admin.site.register(MovieOwnership)
admin.site.register(Payment)
admin.site.register(PaymentItem)
