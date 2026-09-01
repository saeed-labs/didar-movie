from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from movies.models import MoviesModel
from .manager import UserManager



class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="ایمیل", max_length=255, unique=True,)
    username = models.CharField(max_length=255, unique=True, verbose_name="نام کاربری")
    phone = models.CharField(max_length=11, unique=True, verbose_name='تلفن همراه')
    full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="نام کامل")
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_admin = models.BooleanField(default=False, verbose_name='مدیر')
    is_superuser = models.BooleanField(default=False, verbose_name='سوپر یوزر')

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name='تایید شده')
    is_banned = models.BooleanField(default=False, verbose_name='مسدود شده')
    is_special = models.BooleanField(default=False, verbose_name='ویژه')
    special_expires_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ انقضای ویژه')

    @property
    def special_is_active(self):
        if not self.is_special:
            return False

        if not self.special_expires_at:
            return False

        return timezone.now() < self.special_expires_at


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل کاربران'


class MovieOwnership(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='movie_ownerships')
    movie = models.ForeignKey(MoviesModel, on_delete=models.PROTECT, related_name='owners')
    payment = models.ForeignKey('payment.Payment', on_delete=models.PROTECT, related_name='ownerships')
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


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام اشتراک')
    duration_days = models.PositiveIntegerField(verbose_name='مدت اشتراک')
    price = models.PositiveBigIntegerField(verbose_name='قیمت')
    is_active = models.BooleanField(default=True,verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'پلن اشتراک'
        verbose_name_plural = 'پلن‌های اشتراک'

class UserOTPModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')
    otp_code = models.PositiveBigIntegerField(unique=True, verbose_name='کد تایید')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.user.username

    def expired_otp(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=2)

    class Meta:
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کدهای تایید'
        ordering = ('-created_at',)


class RegisterUserOTPModel(models.Model):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    username = models.CharField(max_length=32, verbose_name='نام کاربری')
    phone = models.CharField(max_length=11, verbose_name='تلفن همراه')
    password = models.CharField(max_length=32, verbose_name='پسورد', null=True, blank=True)
    code = models.PositiveIntegerField(verbose_name='کد تایید')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def expired_otp(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=2)

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = 'کد تایید ثبت نام'
        verbose_name_plural = 'کدهای تایید ثبت نام'
        ordering = ('-created_at',)
