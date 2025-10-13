# db_utilities.py

class db_utilities:
    def __init__(self, cursor):
        self.cursor = cursor

    def delete_from_table(self, table_name, condition_column, condition_value):
        sql = f"DELETE FROM {table_name} WHERE {condition_column} = ?"
        self.cursor.execute(sql, (condition_value,))

    def check_requirement_exists(self, check_table, check_column, check_value):
        sql = f"SELECT 1 FROM {check_table} WHERE {check_column} = ? LIMIT 1"
        self.cursor.execute(sql, (check_value,))
        return self.cursor.fetchone() is not None

    def update_row(self, table_name, set_column, set_value, condition_column, condition_value):
        sql = f"UPDATE {table_name} SET {set_column} = ? WHERE {condition_column} = ?"
        self.cursor.execute(sql, (set_value, condition_value))