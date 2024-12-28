import sqlite3

DB_PATH = 'db/tasks_management.db'

def execute_query(query, params=None):
    """Виконує SQL-запит і повертає результат."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

# Запити
def get_tasks_by_user(user_id):
    query = "SELECT * FROM tasks WHERE user_id = ?;"
    return execute_query(query, (user_id,))

def get_tasks_by_status(status_name):
    query = """
    SELECT * FROM tasks 
    WHERE status_id = (SELECT id FROM status WHERE name = ?);
    """
    return execute_query(query, (status_name,))

def update_task_status(task_id, new_status):
    query = """
    UPDATE tasks 
    SET status_id = (SELECT id FROM status WHERE name = ?) 
    WHERE id = ?;
    """
    execute_query(query, (new_status, task_id))
    print(f"Task {task_id} updated to status '{new_status}'.")

def get_users_without_tasks():
    query = """
    SELECT * FROM users 
    WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);
    """
    return execute_query(query)

def add_new_task(title, description, status_name, user_id):
    query = """
    INSERT INTO tasks (title, description, status_id, user_id) 
    VALUES (?, ?, (SELECT id FROM status WHERE name = ?), ?);
    """
    execute_query(query, (title, description, status_name, user_id))
    print(f"Task '{title}' added successfully.")

def get_uncompleted_tasks():
    query = """
    SELECT * FROM tasks 
    WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
    """
    return execute_query(query)

def delete_task(task_id):
    query = "DELETE FROM tasks WHERE id = ?;"
    execute_query(query, (task_id,))
    print(f"Task {task_id} deleted.")

def find_users_by_email(email_pattern):
    query = "SELECT * FROM users WHERE email LIKE ?;"
    return execute_query(query, (email_pattern,))

def update_user_fullname(user_id, new_name):
    query = "UPDATE users SET fullname = ? WHERE id = ?;"
    execute_query(query, (new_name, user_id))
    print(f"User {user_id} updated with new name '{new_name}'.")

def count_tasks_by_status():
    query = """
    SELECT status.name, COUNT(tasks.id) 
    FROM tasks
    JOIN status ON tasks.status_id = status.id
    GROUP BY status.name;
    """
    return execute_query(query)

def get_tasks_by_email_domain(domain):
    query = """
    SELECT tasks.* 
    FROM tasks
    JOIN users ON tasks.user_id = users.id
    WHERE users.email LIKE ?;
    """
    return execute_query(query, (f"%{domain}",))

def get_tasks_without_description():
    query = "SELECT * FROM tasks WHERE description IS NULL OR description = '';"
    return execute_query(query)

def get_users_with_in_progress_tasks():
    query = """
    SELECT users.fullname, tasks.title 
    FROM tasks
    JOIN users ON tasks.user_id = users.id
    WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress');
    """
    return execute_query(query)

def count_tasks_for_each_user():
    query = """
    SELECT users.fullname, COUNT(tasks.id) 
    FROM users
    LEFT JOIN tasks ON users.id = tasks.user_id
    GROUP BY users.id;
    """
    return execute_query(query)

# Приклад виклику функцій
if __name__ == "__main__":
    print(get_tasks_by_user(1))
    print(get_tasks_by_status('new'))
    update_task_status(1, 'in progress')
    print(get_users_without_tasks())
    add_new_task('New Task', 'This is a new task description', 'new', 1)
    print(get_uncompleted_tasks())
    delete_task(2)
    print(find_users_by_email('%@example.com'))
    update_user_fullname(1, 'Updated Name')
    print(count_tasks_by_status())
    print(get_tasks_by_email_domain('@example.com'))
    print(get_tasks_without_description())
    print(get_users_with_in_progress_tasks())
    print(count_tasks_for_each_user())
    