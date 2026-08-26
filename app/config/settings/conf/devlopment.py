from .paths import BASE_DIR

STATIC_URL = "/assets/static/"
STATIC_ROOT = BASE_DIR.parent / "volumes" / "assets" / "static/"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'volumes' / 'media'

SPECTACULAR_SETTINGS = {
    'TITLE': 'دیدار موی',
    'DESCRIPTION': 'API دیدار',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
    # 'SWAGGER_UI_DIST': 'دیدار موی',
    # 'SWAGGER_UI_FAVICON_HREF': 'API دیدار',
    # 'REDOC_DIST': 'دیدار موی',
    # OTHER SETTINGS
}



REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

#
#
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = True



# Maximum request body size (100 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024

# Maximum size of uploaded file kept in memory (100 MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024

