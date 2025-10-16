# export_tools.py

from ..dataman.db_json_bridge import dump_db_to_json
from ..dataman.export_db_to_csv import export_db_to_csv
from database.core.paths import DATA_DIR, JSON_DUMP, CSV_DIR

def export_db_to_json_interactive(db_name: str) -> None:
    """
    Export DB → JSON to a fixed, non-overridable path:
        database/data/database_dump.json
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    dump_db_to_json(db_name, str(JSON_DUMP))
    print(f"✅ Exported JSON → {JSON_DUMP}")

def export_db_to_csv_interactive() -> None:
    """
    Export all tables → CSVs into a fixed folder:
        database/data/csv_exports/
    """
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    export_db_to_csv(str(CSV_DIR))  # delimiter=';' already set in your exporter
    print(f"✅ Exported CSVs → {CSV_DIR}")
