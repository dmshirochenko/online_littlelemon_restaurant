#!/usr/bin/env bash

set -e

# Wait for Postgres
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Waiting for postgres..."
  sleep 5
done

chown www-data:www-data /var/log

python manage.py collectstatic --noinput

if [ "${DJANGO_COLLECT_MIGRATE}" -eq "1" ]; then
  echo "Django migration is up"
  python manage.py migrate
fi

# Replace uwsgi with gunicorn
gunicorn littlelemon.wsgi:application --bind 0.0.0.0:8000 --workers=4
