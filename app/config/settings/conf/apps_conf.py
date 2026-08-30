DJANGO_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [

    'drf_spectacular',
    'drf_spectacular_sidecar',
    'django_filters',
]

LOCAL_APPS = [
    'accounts.apps.AccountsConfig',
    'movies.apps.MoviesConfig',
    'categories.apps.CategoriesConfig',
    'cart.apps.CartConfig',
    'payment.apps.PaymentConfig',

]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS
