#!/bin/sh

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Gunicorn server
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000