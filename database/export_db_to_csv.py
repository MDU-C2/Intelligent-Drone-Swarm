# export_db_to_csv.py
"""
Export all user tables from the active SQLite database to CSV files.

Usage:
    python export_db_to_csv.py
"""

import csv
import os
import pathlib
from connect_database import connect_database


def _list_user_tables(cursor):
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    return [r[0] for r in cursor.fetchall()]


def export_db_to_csv(output_dir="csv_exports"):
    """Export every user table in the active DB (from db_name.txt) to CSVs."""
    db_name_file = pathlib.Path("db_name.txt")
    if not db_name_file.exists():
        raise FileNotFoundError("db_name.txt not found — run setup_database.py first.")
    db_path = db_name_file.read_text().strip()
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")

    os.makedirs(output_dir, exist_ok=True)

    with connect_database(db_path) as db:
        tables = _list_user_tables(db.cursor)
        if not tables:
            print("No tables found in the database.")
            return

        for table in tables:
            db.cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in db.cursor.fetchall()]

            db.cursor.execute(f"SELECT * FROM {table}")
            rows = db.cursor.fetchall()

            out_path = os.path.join(output_dir, f"{table}.csv")
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(columns)
                writer.writerows(rows)

            print(f"Exported {table} → {out_path}")

    print(f"\nAll tables exported successfully to folder: {output_dir}")


if __name__ == "__main__":
    export_db_to_csv()
