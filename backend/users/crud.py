from backend.db import get_db_connection


def add_user(username: str, password: str):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as curs:
            curs.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id", (username, password, ))
            user_id = curs.fetchone()[0]
    return user_id


def get_current_user(user_id: int):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as curs:
            curs.execute("SELECT id, username FROM users WHERE id = (%s)", (user_id,))
            user = curs.fetchone()
    return user


def get_user_hash_password(username: str):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as curs:
            curs.execute("SELECT id, username, password FROM users WHERE username = (%s)", (username,))
            user = curs.fetchone()
        return user
