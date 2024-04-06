# import sqlite3

# def create_connection() -> sqlite3.Connection:
#     # create a database connection to a SQLite database
#     return sqlite3.connect("../natural_nails.db")

import queue
import sqlite3
from contextlib import contextmanager

class ConnectionPool:
    def __init__(self, max_connections, database):
        self.max_connections = max_connections
        self.database = database
        self.pool = queue.Queue(maxsize=max_connections)

        for _ in range(max_connections):
            conn = self.create_connection()
            self.pool.put(conn)

    def create_connection(self):
        return sqlite3.connect(self.database)

    def get_connection(self, timeout):
        try:
            return self.pool.get(timeout=timeout)
        except queue.Empty:
            raise RuntimeError("Timeout: No available connections in the pool.")

    def release_connection(self, conn):
        self.pool.put(conn)

    @contextmanager
    def connection(self, timeout=10):
        conn = self.get_connection(timeout)
        try:
            yield conn
        finally:
            self.release_connection(conn)
        
    

# initialize connection pool
pool = ConnectionPool(12, '../natural_nails.db')
