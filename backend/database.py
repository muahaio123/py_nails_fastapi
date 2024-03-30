import sqlite3

conn = None
def create_connection():
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect("natural_nails.db")
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)

def getDBConnection():
    return conn

def close_connection():
    if conn:
        conn.close()
