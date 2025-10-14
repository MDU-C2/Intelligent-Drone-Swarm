# export_tools.py

from ..dataman.db_json_bridge import dump_db_to_json
from ..dataman.export_db_to_csv import export_db_to_csv
from .paths import DATA_DIR, JSON_DUMP, CSV_DIR

def export_db_to_json_interactive(db_name: str) -> None:
    """
    Export DB → JSON to a fixed, non-overridable path:
        database/data/database_dump.json
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DATA_DIR / "database_dump.json"          # fixed
    dump_db_to_json(db_name, str(out_path))
    print(f"✅ Exported JSON → {out_path}")

def export_db_to_csv_interactive() -> None:
    """
    Export all tables → CSVs into a fixed folder:
        database/data/csv_exports/
    """
    out_dir = DATA_DIR / "csv_exports"                  # fixed
    out_dir.mkdir(parents=True, exist_ok=True)
    export_db_to_csv(str(out_dir))  # your writer uses delimiter=';'
    print(f"✅ Exported CSVs → {out_dir}")
