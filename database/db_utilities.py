# db_utilities.py

import sqlite3

class db_utilities:
    def __init__(self, cursor):
        self.cursor = cursor

    # --- Existing methods (delete, update, check, etc.) stay the same ---

    def list_tables(self):
        """Return a list of user tables (excluding sqlite_sequence)."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        return [row[0] for row in self.cursor.fetchall() if row[0] != "sqlite_sequence"]

    def list_columns(self, table_name):
        """Return a list of columns for a given table."""
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        return [row[1] for row in self.cursor.fetchall()]

    def search_value(self, table_name, column_name, value, partial=False):
        """
        Search a table for a given value (exact or partial match).

        Args:
            table_name (str): Table to search.
            column_name (str): Column to check.
            value (str): Value or pattern to look for.
            partial (bool): If True, performs case-insensitive partial match using LIKE.

        Returns:
            list[tuple]: All matching rows (empty list if none found)
        """
        if partial:
            sql = f"SELECT * FROM {table_name} WHERE {column_name} LIKE ? COLLATE NOCASE"
            pattern = f"%{value}%"
            self.cursor.execute(sql, (pattern,))
        else:
            sql = f"SELECT * FROM {table_name} WHERE {column_name} = ?"
            self.cursor.execute(sql, (value,))
        return self.cursor.fetchall()
