import sys
import os

# Додаємо шлях до кореневої папки проєкту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import sqlite3
from faker import Faker

fake = Faker()

def seed_database():
    conn = sqlite3.connect('db/tasks_management.db')
    cursor = conn.cursor()

    # Додавання статусів
    statuses = [('new',), ('in progress',), ('completed',)]
    cursor.executemany('INSERT OR IGNORE INTO status (name) VALUES (?);', statuses)

    # Додавання користувачів
    users = [(fake.name(), fake.unique.email()) for _ in range(10)]
    cursor.executemany('INSERT INTO users (fullname, email) VALUES (?, ?);', users)

    # Додавання завдань
    cursor.execute('SELECT id FROM status')
    status_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT id FROM users')
    user_ids = [row[0] for row in cursor.fetchall()]

    tasks = [
        (fake.sentence(nb_words=6), fake.text(), fake.random.choice(status_ids), fake.random.choice(user_ids))
        for _ in range(20)
    ]
    cursor.executemany('INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?);', tasks)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_database()
