import os
from dotenv import load_dotenv

load_dotenv()

from .apps_conf import INSTALLED_APPS
from .meddleware_conf import MIDDLEWARE
from .db_conf import DATABASES
from .devlopment import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', )

DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'OPTIONS': {
            'host': os.environ.get('DJANGO_EMAIL_HOST'),
            'port': int(os.environ.get('DJANGO_EMAIL_PORT', 587)),
            'username': os.environ.get('DJANGO_EMAIL_HOST_USER'),
            'password': os.environ.get('DJANGO_EMAIL_HOST_PASSWORD'),
            'use_tls': os.environ.get('DJANGO_EMAIL_USE_TLS','True',).lower() == 'true',
        },
    },
}

DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL')


#
# EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
# EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT', 587))
# EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS', 'True').lower() == 'true'
# EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL')
#



AUTH_USER_MODEL = "accounts.User"
