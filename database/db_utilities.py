# db_utilities.py

import sqlite3

class db_utilities:
    def __init__(self, cursor):
        self.cursor = cursor

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

    def pretty_print_rows(self, table_name, rows, max_cell_len=60, ellipsis="…"):
        """
        Nicely print query results in a formatted table with column headers.

        Args:
            table_name (str): Table whose schema will be used for headers.
            rows (list[tuple]): Result rows to print.
            max_cell_len (int): Max characters per cell before truncation.
            ellipsis (str): Ellipsis string to append when truncating.
        """
        if not rows:
            print("No data found.")
            return

        # Fetch column names dynamically
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        headers = [row[1] for row in self.cursor.fetchall()]
        num_cols = len(headers)

        # Some queries (SELECT *) will match; safeguard if tuple length differs
        max_cols = max(num_cols, len(rows[0]))
        if len(headers) < max_cols:
            headers += [f"col{i+1}" for i in range(len(headers), max_cols)]

        def _to_str(x):
            return "" if x is None else str(x)

        def _truncate(s):
            # Truncate at max_cell_len and add ellipsis if needed
            if len(s) <= max_cell_len:
                return s
            # keep room for ellipsis itself
            cut = max_cell_len - len(ellipsis)
            return (s[:cut] + ellipsis) if cut > 0 else s[:max_cell_len]

        # Prepare truncated display rows
        display_rows = []
        for row in rows:
            display_rows.append([_truncate(_to_str(row[i])) for i in range(len(row))])

        # Compute max width per column using truncated rows
        col_widths = []
        for i in range(max_cols):
            header = headers[i]
            column_cells = [r[i] for r in display_rows if i < len(r)]
            max_data_len = max([len(header)] + [len(c) for c in column_cells] or [len(header)])
            col_widths.append(max(max_data_len, 8))  # minimum width 8 for readability

        # Render header
        header_line = " | ".join(headers[i].ljust(col_widths[i]) for i in range(max_cols))
        divider = "-+-".join("-" * col_widths[i] for i in range(max_cols))
        print("\n" + header_line)
        print(divider)

        # Render rows
        for r in display_rows:
            line = " | ".join(
                (r[i] if i < len(r) else "").ljust(col_widths[i]) for i in range(max_cols)
            )
            print(line)

    def delete_from_table (self,table_name, condition_column, condition_value): 
        self.cursor.execute(
            f"""
            DELETE FROM {table_name} WHERE {condition_column} = ?
            """,
            (condition_value,)
        ) 
 
    def check_requirement_exists (self, check_table, check_column, check_value):
        self.cursor.execute(
            f"SELECT 1 FROM {check_table} WHERE {check_column} = ?",
            (check_value,)
        )
        return self.cursor.fetchone()
    
    def update_row(self, table, condition_column, condition_value, update_column, new_value):
         self.cursor.execute(
            f"""
            UPDATE {table}
            SET {update_column} = ?
            WHERE {condition_column} = ?
            """,
            (new_value, condition_value)
        )