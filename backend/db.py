import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
            host="db_todo",
            database="todo",
            user='postgres',
            password='postgres')

    return conn