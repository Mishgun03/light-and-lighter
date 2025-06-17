import os
import time
import socket
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

host = os.getenv('MYSQL_HOST')
port = int(os.getenv('MYSQL_PORT'))
timeout = 1

print(f"Waiting for database at {host}:{port}...")

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        print("Database is available!")
        break
    except socket.error as ex:
        print(f"Database isn't available yet. Retrying... Error: {ex}")
        time.sleep(1)
