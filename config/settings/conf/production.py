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


# AUTH_USER_MODEL = "accounts.User"


