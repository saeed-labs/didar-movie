from rest_framework import serializers
from accounts.models import SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "name",
            "duration_days",
            "price",
        ]