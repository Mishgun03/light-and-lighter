#!/bin/sh
set -e

echo "--- Running wait_for_db.py ---"
python /app/wait_for_db.py

echo "--- Running migrations ---"
python /app/manage.py migrate --noinput

echo "--- Running pytest ---"
pytest

echo "--- Test script finished ---"