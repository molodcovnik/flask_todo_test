from backend.db import get_db_connection


def get_current_todo(user_id: int, todo_id: int):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as curs:
            curs.execute("SELECT id, title, description, created_at FROM todos WHERE user_id = (%s) AND id = (%s)",
                         (user_id, todo_id))
            todo = curs.fetchone()
    return todo


def get_user_todos(user_id: int):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as curs:
            curs.execute("SELECT id, title, description, created_at FROM todos WHERE user_id = (%s)", (user_id,))
            todos = curs.fetchall()
    return todos


def create_todo(title: str, desc: str, user_id: int):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as curs:
            curs.execute("INSERT INTO todos (title, description, user_id) VALUES (%s, %s, %s) RETURNING id;", (title, desc, user_id,))
            todo_id = curs.fetchone()[0]
    return todo_id


def delete_todo(todo_id: int):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as curs:
            curs.execute("DELETE FROM todos where id = (%s);", (todo_id,))


def get_author_todo(todo_id: int, user_id: int):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as curs:
            curs.execute("SELECT id FROM todos WHERE id = %s AND user_id = %s ORDER BY created_at DESC;", (todo_id, user_id, ))
            todo = curs.fetchone()
    return todo


def update_todo(todo_id: int, title: str, description: str, created_at: str):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as curs:
            curs.execute("UPDATE todos set id = %s, title = %s, description = %s, created_at = %s WHERE id = %s", (todo_id, title, description, created_at, todo_id,))