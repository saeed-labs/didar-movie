from django.core.mail import send_mail
from django.conf import settings


def send_login_otp_email(email, code):
    send_mail(
        subject="کد تایید ورود",
        message=f"""
کد تایید ورود شما:

{code}

این کد تا چند دقیقه معتبر است.
اگر شما درخواست ورود نداده‌اید، این ایمیل را نادیده بگیرید.
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


def send_register_otp_email(email, code):
    send_mail(
        subject="کد تایید ثبت نام",
        message=f"""
کد تایید ثبت نام شما:

{code}

این کد تا چند دقیقه معتبر است.
اگر شما درخواست ورود نداده‌اید، این ایمیل را نادیده بگیرید.
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


def send_password_reset_email(email, code):
    send_mail(
        subject="بازیابی رمز عبور",
        message=f"کد بازیابی شما: {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )


def send_change_email_otp(email, code):
    send_mail(
        subject="تغییر ایمیل حساب کاربری",
        message=f"""
کد تایید تغییر ایمیل:

{code}

این کد تا ۵ دقیقه معتبر است.
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
