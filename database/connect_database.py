# connect_database.py

import sqlite3

class connect_database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name, isolation_level=None)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")  # Enforce foreign keys
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
        