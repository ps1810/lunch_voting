#!/bin/sh

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py shell << EOF
from django.contrib.auth import get_user_model
import os
User = get_user_model()
if not User.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists():
    User.objects.create_superuser(
        os.environ['DJANGO_SUPERUSER_USERNAME'],
        os.environ['DJANGO_SUPERUSER_EMAIL'],
        os.environ['DJANGO_SUPERUSER_PASSWORD']
    )
EOF

# Start the Gunicorn server
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000