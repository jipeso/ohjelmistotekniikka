import sqlite3
from config import DATABASE_FILE_PATH

database_connection = sqlite3.connect(DATABASE_FILE_PATH)
database_connection.row_factory = sqlite3.Row


def get_database_connection():
    return database_connection
