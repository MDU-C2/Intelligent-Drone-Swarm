# other_functions.py

class other_functions:
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

# Update requirement
# Finns ett SQL kommando som uppdaterar "originalet"