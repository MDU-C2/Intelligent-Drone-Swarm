# database/app/setup_database.py
from __future__ import annotations

import os
from pathlib import Path
from ..core.connect_database import connect_database
from ..core.create_tables import create_tables
from .paths import DATA_DIR, DB_NAME_TXT  # DATA_DIR = .../database/data ; DB_NAME_TXT = .../database/data/db_name.txt

DEFAULT_DB_NAME = "testing.db"

def _sanitize_filename(name: str) -> str:
    """Ensure we only use a filename (strip any directories) and end with .db."""
    base = Path(name.strip() or DEFAULT_DB_NAME).name  # drop any path parts user typed
    if not base.lower().endswith(".db"):
        base += ".db"
    return base

def main():
    # Make sure data/ exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Ask for DB filename (no directories). Always place it under data/
    print(f"Enter database filename (no path) [{DEFAULT_DB_NAME}]: ", end="")
    user_in = input().strip() or DEFAULT_DB_NAME
    filename = _sanitize_filename(user_in)
    db_path = (DATA_DIR / filename).resolve()

    # Overwrite prompt if the file exists
    if db_path.exists():
        ans = input(f"'{db_path.name}' already exists in data/. Overwrite? (y/N): ").strip().lower()
        if ans != "y":
            print("Cancelled. No changes made.")
            return
        os.remove(db_path)

    # Persist absolute path so the whole app consistently finds the DB
    DB_NAME_TXT.write_text(str(db_path), encoding="utf-8")
    print(f"→ Wrote active DB path to {DB_NAME_TXT}:")
    print(f"   {db_path}")

    # Create a fresh database with all tables
    with connect_database(str(db_path)) as db:
        create_tables(db.cursor).create_all_tables()

    print(f"✅ Database initialized at {db_path}")

if __name__ == "__main__":
    main()
