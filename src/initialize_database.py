from database_connection import get_database_connection


def reset_database(conn):
    cursor = conn.cursor()
    cursor.execute("drop table if exists articles")
    conn.commit()


def setup_database(conn):
    cursor = conn.cursor()
    cursor.execute("""
        create table articles (
            id integer primary key,
            title text,
            content text,
            url text
        )
    """)

    conn.commit()


def initialize_database():
    conn = get_database_connection()

    reset_database(conn)
    setup_database(conn)


if __name__ == "__main__":
    initialize_database()
