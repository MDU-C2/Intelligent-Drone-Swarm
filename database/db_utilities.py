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

    def pretty_print_rows(self, table_name, rows):
        """
        Nicely print query results in a formatted table with column headers.
        """
        if not rows:
            print("No data found.")
            return

        # Fetch column names dynamically
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        headers = [row[1] for row in self.cursor.fetchall()]
        num_cols = len(headers)

        # Handle case where returned rows may not include all columns
        max_cols = max(num_cols, len(rows[0]))
        if len(headers) < max_cols:
            headers += [f"col{i+1}" for i in range(len(headers), max_cols)]

        # Compute max width per column (header vs value)
        col_widths = []
        for i in range(max_cols):
            col_data = [str(row[i]) if row[i] is not None else "" for row in rows]
            max_data_len = max([len(h) for h in [headers[i]]] + [len(x) for x in col_data])
            col_widths.append(max(max_data_len, 8))  # minimum width 8

        # Header line
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        divider = "-+-".join("-" * col_widths[i] for i in range(max_cols))

        print("\n" + header_line)
        print(divider)

        # Data rows
        for row in rows:
            line = " | ".join(
                (str(row[i]) if row[i] is not None else "").ljust(col_widths[i])
                for i in range(len(row))
            )
            print(line)
