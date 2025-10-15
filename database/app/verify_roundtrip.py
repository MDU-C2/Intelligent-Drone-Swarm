from __future__ import annotations
import shutil, tempfile
from pathlib import Path

from ..dataman.db_json_bridge import dump_db_to_json, restore_db_from_json
from ..core.connect_database import connect_database
from database.core.paths import DATA_DIR, DB_NAME_TXT, ROUNDTRIP_DUMP

def _read_active_db_path() -> Path:
    if not DB_NAME_TXT.exists():
        raise SystemExit(f"db_name.txt not found at {DB_NAME_TXT}")
    db_path = Path(DB_NAME_TXT.read_text().strip())
    if not db_path.exists():
        raise SystemExit(f"Active DB not found: {db_path}")
    return db_path

def _fetch_all_tables(conn) -> dict[str, list[tuple]]:
    cur = conn.cursor
    cur.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    tables = [r[0] for r in cur.fetchall()]
    snapshot = {}
    for t in tables:
        cur.execute(f"PRAGMA table_info({t})")
        cols = [c[1] for c in cur.fetchall()]
        cur.execute(f"SELECT * FROM {t} ORDER BY rowid")
        rows = cur.fetchall()
        snapshot[t] = (cols, rows)
    return snapshot

def _compare_snapshots(a: dict, b: dict) -> None:
    a_tables = set(a.keys()); b_tables = set(b.keys())
    if a_tables != b_tables:
        missing_in_b = sorted(a_tables - b_tables)
        extra_in_b   = sorted(b_tables - a_tables)
        raise SystemExit(f"Table mismatch.\nMissing in restored: {missing_in_b}\nExtra in restored: {extra_in_b}")
    for t in sorted(a_tables):
        a_cols, a_rows = a[t]; b_cols, b_rows = b[t]
        if a_cols != b_cols:
            raise SystemExit(f"Column mismatch in table '{t}':\n  src={a_cols}\n  dst={b_cols}")
        if a_rows != b_rows:
            raise SystemExit(f"Row mismatch in table '{t}' (counts: src={len(a_rows)}, dst={len(b_rows)}).")

def run_roundtrip_check() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db_path = _read_active_db_path()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        dump_path = tmpdir / "dump.json"
        restored_db = tmpdir / "restored.db"

        print(f"→ Dumping {db_path.name} → {dump_path}")
        dump_db_to_json(str(db_path), str(dump_path))

        # Keep a copy in data/ (fixed, non-overridable)
        shutil.copyfile(dump_path, ROUNDTRIP_DUMP)
        print(f"   (Saved copy) {ROUNDTRIP_DUMP}")

        print(f"→ Restoring {dump_path} → {restored_db}")
        restore_db_from_json(str(restored_db), str(dump_path), overwrite=True)

        print("→ Comparing source vs restored …")
        with connect_database(str(db_path)) as src, connect_database(str(restored_db)) as dst:
            snap_src = _fetch_all_tables(src)
            snap_dst = _fetch_all_tables(dst)
        _compare_snapshots(snap_src, snap_dst)

    print("✅ Round-trip verification PASSED.")

if __name__ == "__main__":
    run_roundtrip_check()
