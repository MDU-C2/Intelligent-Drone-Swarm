# setup_database.py
# Usage: Run ONCE when setting up the database for the project. Type in to terminal "python setup_database.py"

# Ask user for database name

from connect_database import connect_database
from create_tables import create_tables

if __name__ == "__main__":

    print("Please enter the name of the database you want to create (with .db):\n") 
    db_name = input().strip()
    try:
        if not db_name.endswith(".db"):
            raise ValueError("Database name must end with .db")
        with open("db_name.txt", "w") as f:
            f.write(db_name)
        print(f"Database name '{db_name}' successfully written to db_name.txt.")
        with connect_database(db_name) as db:
            tables = create_tables(db.cursor)
            tables.create_all_tables()
            print("Database and all tables created successfully!")
    except Exception as e:
        print(f"Error writing to db_name.txt: {e}, please try again.")
        exit(1)