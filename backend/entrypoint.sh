#!/bin/sh

FLAG_FILE="/tmp/db_initialized.flag"

echo "Waiting for mysql..."

python wait_for_db.py

echo "MySQL started"

echo "Applying database migrations..."
python manage.py migrate

echo "Starting Django server in background..."
python manage.py runserver 0.0.0.0:8000 &
# Сохраняем PID (ID процесса) сервера, чтобы потом его можно было "вернуть"
SERVER_PID=$!

echo "Waiting for server to start..."
sleep 5

if [ ! -f "$FLAG_FILE" ]; then
    echo "First time setup: creating superuser and populating data..."

    # Создаем суперпользователя
    python manage.py createsuperuser --noinput

    # Запускаем команду для заполнения БД
    python manage.py populate_items

    # Создаем флаг, чтобы этот блок не выполнялся снова
    touch $FLAG_FILE
    echo "First time setup complete."
else
    echo "Database already initialized. Skipping first time setup."
fi

echo "Bringing server to foreground..."
wait $SERVER_PID