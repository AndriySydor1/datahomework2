import sys
import os
import sqlite3
from seed import seed_database

DB_PATH = 'db/tasks_management.db'

def test_seed_data():
    """Перевіряє, чи скрипт seed.py заповнив базу даних."""
    # Додаємо шлях до кореневої директорії
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    
    # Запускаємо seed.py
    seed_database()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Перевіряємо, чи є користувачі
    cursor.execute("SELECT COUNT(*) FROM users;")
    users_count = cursor.fetchone()[0]
    assert users_count > 0

    # Перевіряємо, чи є статуси
    cursor.execute("SELECT COUNT(*) FROM status;")
    status_count = cursor.fetchone()[0]
    assert status_count > 0

    # Перевіряємо, чи є завдання
    cursor.execute("SELECT COUNT(*) FROM tasks;")
    tasks_count = cursor.fetchone()[0]
    assert tasks_count > 0

    conn.close()
    