#!/usr/bin/env bash
set -euo pipefail

python /app/manage.py migrate --noinput
python /app/manage.py collectstatic --noinput || true

if [ "${DJANGO_DEBUG:-False}" = "True" ]; then
  python /app/manage.py runserver 0.0.0.0:8000
else
  gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi


