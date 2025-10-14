# paths.py

from pathlib import Path

# Package root = .../database/
ROOT = Path(__file__).resolve().parents[1]

# Fixed data directory
DATA_DIR = ROOT / "data"

# Canonical files/dirs inside data/
DB_PATH         = DATA_DIR / "testing.db"               # active DB
DB_NAME_TXT     = DATA_DIR / "db_name.txt"              # stores absolute path to DB
JSON_DUMP       = DATA_DIR / "database_dump.json"       # “normal” export target
ROUNDTRIP_DUMP  = DATA_DIR / "roundtrip_last_dump.json" # copy kept by round-trip check
CSV_DIR         = DATA_DIR / "csv_exports"              # CSV exports folder
