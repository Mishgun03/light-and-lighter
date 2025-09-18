#!/usr/bin/env bash
set -e


echo "--- Running migrations ---"
python /app/manage.py migrate --noinput
python /app/manage.py collectstatic --noinput || true

echo "--- Running pytest ---"
pytest

echo "--- Test script finished ---"