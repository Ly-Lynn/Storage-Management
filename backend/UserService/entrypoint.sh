#!/bin/sh

echo "Applying database migrations..."
python manage.py migrate

# echo "Creating superuser..."
# export DJANGO_SUPERUSER_PASSWORD=123 && python manage.py createsuperuser --noinput --username admin --email admin@example.com

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
