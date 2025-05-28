#!/bin/sh

echo "Waiting for database..."
python manage.py wait_for_db

echo "Applying migrations..."
python manage.py migrate

# Fix volume permissions (if needed)
echo "Setting permissions for /vol/web"
mkdir -p /vol/web/media/uploads
chmod -R 775 /vol/web
chown -R django-user:django-user /vol/web

echo "Starting server..."
python manage.py runserver 0.0.0.0:8001
