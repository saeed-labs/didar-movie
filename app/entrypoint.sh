#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE=config.settings

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
#python manage.py compilemessages



python manage.py shell <<EOF
from django.contrib.auth import get_user_model


User = get_user_model()

if User.objects.count() == 0:
    User.objects.create_superuser(
        email="admin@example.com",
        username="admin",
        phone="09123456789",
        password="admin"
    )
    print("Superuser created")
else:
    print("Users already exist, skipping superuser creation")
EOF

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
# python manage.py runserver 0.0.0.0:8000