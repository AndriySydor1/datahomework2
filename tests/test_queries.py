import sqlite3

DB_PATH = 'db/tasks_management.db'

def test_database_connection():
    """Перевіряє, чи база даних доступна для з'єднання."""
    conn = sqlite3.connect(DB_PATH)
    assert conn is not None
    conn.close()

def test_users_table_exists():
    """Перевіряє, чи існує таблиця users у базі даних."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table = cursor.fetchone()
    assert table is not None
    conn.close()

def test_insert_user():
    """Перевіряє можливість додавання користувача до таблиці users."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (fullname, email) VALUES (?, ?);", 
                   ("Test User", "testuser@example.com"))
    conn.commit()

    cursor.execute("SELECT * FROM users WHERE email = ?;", ("testuser@example.com",))
    user = cursor.fetchone()
    assert user is not None
    assert user[1] == "Test User"  # Перевірка fullname
    assert user[2] == "testuser@example.com"  # Перевірка email

    conn.close()
    