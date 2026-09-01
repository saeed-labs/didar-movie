from django.utils import timezone
from rest_framework import permissions
from accounts.models import MovieOwnership, UserProfile


class CanAccessMovie(permissions.BasePermission):
    message = "شما دسترسی به این فیلم ندارید."

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and (
                request.user.profile.is_special or MovieOwnership.objects.filter(user=request.user,
                                                                                 movie=obj).exists()):
            return True
        return False
