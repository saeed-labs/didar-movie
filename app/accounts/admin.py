from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, UserProfile, UserOTPModel, MovieOwnership, SubscriptionPlan

admin.site.site_header = 'پنل مدیریت دیدار'
admin.site.site_title = 'دیدار موی'
admin.site.index_title = 'به پنل مدیریت دیدار خوش آمدید'


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 1

class MovieOwnershipInline(admin.TabularInline):
    model = MovieOwnership
    extra = 1



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm


    list_display = ["email", "username", "full_name", "is_admin"]
    list_filter = ['email', 'username', 'full_name', 'is_admin', 'is_superuser']
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("اطلاعات شخصی", {"fields": ["username", "full_name", "phone"]}),
        ("مجوزها", {"fields": ["is_admin", "is_superuser", 'is_active']}),


    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "username", "full_name", "phone", "is_active", "is_admin", "is_superuser", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

    inlines = [
        UserProfileInline, MovieOwnershipInline,
    ]


# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ["user", "is_verified", "is_banned", "is_special"]
#     list_filter = ['is_verified', 'is_banned', 'is_special']
#     search_fields = ["user__username", "user__email"]
#     ordering = ["user__username"]
#     filter_horizontal = []
#






# admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(User, UserAdmin)
admin.site.register(UserOTPModel)
admin.site.register(MovieOwnership)
admin.site.register(SubscriptionPlan)
admin.site.unregister(Group)