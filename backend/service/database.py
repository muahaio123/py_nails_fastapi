import sqlite3

conn: sqlite3.Connection = None
def create_connection() -> sqlite3.Connection:
    # create a database connection to a SQLite database (return existing one if have)
    if not conn:
        try:
            conn = sqlite3.connect("../natural_nails.db")
        except sqlite3.Error as e:
            print(e)
    return conn

def getDBConnection():
    return conn if conn else create_connection()

def getDBCursor():
    return conn.cursor() if conn else create_connection().cursor()

def close_connection():
    if conn:
        conn.close()
