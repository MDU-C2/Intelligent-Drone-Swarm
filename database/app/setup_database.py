# setup_database.py

import os
from pathlib import Path
from ..core.connect_database import connect_database
from ..core.create_tables import create_tables

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_NAME_PATH = DATA_DIR / "db_name.txt"

if __name__ == "__main__":
    print("Please enter the name of the database you want to create (with .db):\n")
    db_name = input().strip()
    try:
        if not db_name.endswith(".db"):
            raise ValueError("Database name must end with .db")

        # NEW: ensure data/ exists and place the DB INSIDE it (unless absolute)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        db_path = Path(db_name)
        if not db_path.is_absolute():
            db_path = DATA_DIR / db_path.name  # e.g. database/data/testing.db

        # If file exists and user wants overwrite, remove it (your existing logic may handle this)
        if db_path.exists():
            print(f"Database '{db_path}' already exists. Overwrite? [y/N]")
            if input().strip().lower() != "y":
                raise RuntimeError("Cancelled by user.")
            os.remove(db_path)

        # Write absolute/normalized path into db_name.txt
        with open(DB_NAME_PATH, "w", encoding="utf-8") as f:
            f.write(str(db_path))
        print(f"Database name '{db_path}' successfully written to {DB_NAME_PATH.name}.")

        # Create tables
        with connect_database(str(db_path)) as db:
            tables = create_tables(db.cursor)
            tables.create_all_tables()
            print("Database and all tables created successfully!")

    except Exception as e:
        print(f"Error: {e}. Please try again.")
        exit(1)
