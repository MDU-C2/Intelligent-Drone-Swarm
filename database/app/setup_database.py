# setup_database.py

import os
from pathlib import Path
from ..core.connect_database import connect_database
from ..core.create_tables import create_tables

if __name__ == "__main__":

    DB_NAME_PATH = Path(__file__).resolve().parents[1] / "data" / "db_name.txt"

    print("Please enter the name of the database you want to create (with .db):\n")
    db_name = input().strip()
    try:
        if not db_name.endswith(".db"):
            raise ValueError("Database name must end with .db")

        if os.path.exists(db_name):
            ans = input(f"'{db_name}' already exists. Overwrite? (y/N): ").strip().lower()
            if ans != "y":
                print("Aborted.")
                exit(0)
            os.remove(db_name)

        with open(DB_NAME_PATH, "w", encoding="utf-8") as f:
            f.write(db_name)
        print(f"Database name '{db_name}' successfully written to db_name.txt.")

        with connect_database(db_name) as db:
            tables = create_tables(db.cursor)
            tables.create_all_tables()
            print("Database and all tables created successfully!")

    except Exception as e:
        print(f"Error: {e}. Please try again.")
        exit(1)
