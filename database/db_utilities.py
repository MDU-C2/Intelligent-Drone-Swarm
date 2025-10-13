# db_utilities.py

class db_utilities:
    def __init__(self, cursor):
        self.cursor = cursor

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
# Finns ett SQL kommando som uppdaterar "originalet"