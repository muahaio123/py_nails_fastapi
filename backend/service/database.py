import sqlite3

conn: sqlite3.Connection = sqlite3.connect("../natural_nails.db")
def create_connection() -> sqlite3.Connection:
    global conn
    
    # create a database connection to a SQLite database (return existing one if have)
    try:
        conn = sqlite3.connect("../natural_nails.db")
    except sqlite3.Error as e:
        print(e)

    return conn

def getDBConnection():
    return create_connection()

def getDBCursor():
    return create_connection().cursor()

def close_connection():
    if conn:
        conn.close()
