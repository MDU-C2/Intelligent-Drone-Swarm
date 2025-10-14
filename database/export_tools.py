# export_tools.py
"""
Small wrappers to keep run_database.py clean.
- JSON export (interactive path prompt)
- CSV export (interactive folder prompt)
"""

import os
from db_json_bridge import dump_db_to_json
from export_db_to_csv import export_db_to_csv  # uses delimiter=';' per your update


def export_db_to_json_interactive(db_name: str) -> None:
    default_json = "database_dump.json"
    out_path = input(f"\nOutput JSON path [{default_json}]: ").strip() or default_json
    try:
        dump_db_to_json(db_name, out_path)
        print(f"Exported '{db_name}' → '{out_path}'")
    except Exception as e:
        print(f"Export failed: {e}")


def export_db_to_csv_interactive() -> None:
    out_dir_default = "csv_exports"
    out_dir = input(f"\nOutput folder for CSVs [{out_dir_default}]: ").strip() or out_dir_default
    try:
        os.makedirs(out_dir, exist_ok=True)
        export_db_to_csv(out_dir)
    except Exception as e:
        print(f"CSV export failed: {e}")
