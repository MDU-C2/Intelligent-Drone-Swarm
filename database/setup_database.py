# setup_database.py
# Usage: Run ONCE when setting up the database for the project. Type in to terminal "python setup_database.py"

# Ask user for database name

from connect_database import connect_database
from create_tables import create_tables

if __name__ == "__main__":
    with connect_database("example.db") as db:
        tables = create_tables(db.cursor)
        tables.create_all_tables()
        print("Database and all tables created successfully!")
