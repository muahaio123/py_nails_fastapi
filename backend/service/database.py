import queue
import sqlite3
import logging
import os
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class ConnectionPool:
    def __init__(self, max_connections, database, default_timeout=10):
        self.default_timeout = default_timeout
        self.max_connections = max_connections
        self.database = database
        self.pool = queue.Queue(maxsize=max_connections)

        for _ in range(max_connections):
            conn = self.create_connection()
            self.pool.put(conn)
        logger.info(f"Connection pool initialized with {max_connections} connections to {database}")

    def create_connection(self):
        return sqlite3.connect(self.database, check_same_thread=False, timeout=self.default_timeout)

    def get_connection(self):
        try:
            return self.pool.get(timeout=self.default_timeout)
        except queue.Empty:
            logger.error("No available connections in pool after timeout")
            raise RuntimeError("Timeout: No available connections in the pool.")

    def release_connection(self, conn):
        self.pool.put(conn)

    @contextmanager
    def connection(self):
        conn = self.get_connection()
        try:
            yield conn
        finally:
            self.release_connection(conn)
        
# Initialize connection pool with configurable DB path
db_path = os.getenv('DATABASE_PATH', '../natural_nails.db')
pool = ConnectionPool(12, db_path)
