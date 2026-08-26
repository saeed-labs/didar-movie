from django.urls import path

from .views import UserView, LoginUserView, VerifyUserOTPView, RegisterUserView, VeryfyRegisterUserOTPView

urlpatterns = [
    path('', UserView.as_view()),
    path("login/", LoginUserView.as_view()),
    path("login/verify-otp/", VerifyUserOTPView.as_view()),
    path("register/", RegisterUserView.as_view()),

    path("register/verify/", VeryfyRegisterUserOTPView.as_view()),

]
