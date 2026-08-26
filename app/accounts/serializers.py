from rest_framework import serializers, status
from django.utils import timezone
from datetime import timedelta

from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        # fields = '__all__'
        exclude = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'last_login')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=3)

class VerifyOTPSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.IntegerField()





class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            'phone',
            "password",
            "password2"
        ]

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("پسورد باید حداقل 8 کاراکتر باشد")
        if value == "":
            raise serializers.ValidationError("پسورد نمی‌تواند خالی باشد")
        if value.isdigit():
            raise serializers.ValidationError("پسورد نمی‌تواند فقط شامل اعداد باشد")
        if value.isalpha():
            raise serializers.ValidationError('پسورد نمی تواند فقط شامل حروف باشد')
        if value.isupper():
            raise serializers.ValidationError('پسورد نمی تواند فقط شامل حروف بزرگ باشد')
        if value.islower():
            raise serializers.ValidationError('پسورد نمی تواند فقط شامل حروف کوچک باشد')
        return value

    def validate_phone(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("شماره تلفن باید 11 رقم باشد")
        if not value.isdigit():
            raise serializers.ValidationError("شماره تلفن باید فقط شامل اعداد باشد")
        return value

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("نام کاربری باید حداقل 3 کاراکتر باشد")
        if not value.isalpha():
            raise serializers.ValidationError("نام کاربری باید فقط شامل حروف باشد")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "پسوردها یکسان نیستند"}, code=status.HTTP_400_BAD_REQUEST)

        if attrs['username'] == attrs["password"]:
            raise serializers.ValidationError({"username": "نام کاربری نمی‌تواند با پسورد یکسان باشد"}, code=status.HTTP_400_BAD_REQUEST)
        return attrs

    # def create(self, validated_data):
    #     validated_data.pop("password2")
    #
    #     user = User.objects.create_user(
    #         email=validated_data["email"],
    #         username=validated_data["username"],
    #         phone=validated_data["phone"],
    #         password=validated_data["password"]
    #     )
    #
    #     return user


class VerifyResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=8)



class OTPTimeSerializer(serializers.Serializer):
    time = serializers.SerializerMethodField()

    def get_time(self, obj):

        remaining = (obj.created_at + timedelta(minutes=2)) - timezone.now()
        seconds = max(int(remaining.total_seconds()), 0)
        minutes = seconds // 60
        seconds = seconds % 60

        return f"{minutes:02d}:{seconds:02d}"
