import random

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer, OTPTimeSerializer, VerifyOTPSerializer, RegisterSerializer, VerifyResetOTPSerializer
from .models import User, UserProfile, UserOTPModel, RegisterUserOTPModel
from utils.send_email import send_login_otp_email, send_register_otp_email

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class UserView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.select_related('profile').all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class LoginUserView(APIView):
    serializer_class = LoginSerializer
    throttle_classes = [AnonRateThrottle,]

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(username=email, password=password)

        if not user:
            return Response(
                {
                    "message": "اطلاعات وارد شده نادرست است."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        code = random.randint(1000, 9999)

        last_otp = UserOTPModel.objects.filter(user=user).first()

        if last_otp:
            if not last_otp.expired_otp():
                time_serializer = OTPTimeSerializer(last_otp)
                return Response(
                    {
                        "message": "کد تایید قبلی هنوز معتبر است.",
                        "remaining_time": time_serializer.data["time"],
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

        try:

            send_login_otp_email(user.email, code)

            UserOTPModel.objects.update_or_create(
                user=user,
                defaults={
                    "otp_code": code,
                }
            )

            return Response(
                {
                    "message": "کد تایید با موفقیت ارسال شد.",
                    "user_id": user.id,
                    "otp_code": code,  # فقط development
                },
                status=status.HTTP_200_OK
            )

        except Exception:

            return Response(
                {
                    "message": "کد تایید ارسال نشد."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class VerifyUserOTPView(APIView):
    serializer_class = VerifyOTPSerializer
    throttle_classes = [AnonRateThrottle, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = int(serializer.validated_data["user_id"])
        otp_code = serializer.validated_data["code"]

        otp = UserOTPModel.objects.filter(user_id=user_id, otp_code=otp_code).first()

        if not otp:
            return Response(
                {
                    'message': 'کد اشتباه است.'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        if otp.expired_otp():
            otp.delete()
            return Response(
                {
                    'message': 'کد منقضی شده است.'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        otp.delete()  # حذف کد تایید بعد از استفاده

        refresh = RefreshToken.for_user(otp.user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        )


class RegisterUserView(APIView):
    serializer_class = RegisterSerializer
    throttle_classes = [AnonRateThrottle, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        username = serializer.validated_data["username"]
        phone = serializer.validated_data["phone"]
        password = serializer.validated_data["password"]

        code = random.randint(1000, 9999)

        try:
            send_register_otp_email(email, code)
            RegisterUserOTPModel.objects.update_or_create(
                email=email,
                defaults={
                    "username": username,
                    "phone": phone,
                    "password": password,
                    "code": code,
                }
            )
            return Response({'message': 'کد تایید ارسال شد'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'کد تایید ارسال نشد'}, status=status.HTTP_400_BAD_REQUEST)



class VeryfyRegisterUserOTPView(APIView):
    serializer_class = VerifyResetOTPSerializer
    throttle_classes = [AnonRateThrottle, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        otp = RegisterUserOTPModel.objects.filter(email=email, code=code).first()

        if not otp:
            return Response(
                {
                    'message': 'کد اشتباه است.'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        if otp.expired_otp():
            otp.delete()
            return Response(
                {
                    'message': 'کد منقضی شده است.'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(
            email=email,
            username=otp.username,
            phone=otp.phone,
            password=otp.password
        )
        UserProfile.objects.create(user=user)
        otp.delete()  # حذف کد تایید بعد از استفاده
        return Response({"message": "ثبت نام موفق بود", "user": RegisterSerializer(user).data}, status=201)