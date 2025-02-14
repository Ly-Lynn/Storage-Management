#!/bin/sh

echo "Applying mongodb database migrations..."
python manage.py migrate --fake-initial

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
