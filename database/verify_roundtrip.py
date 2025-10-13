# verify_roundtrip.py
"""
Standalone round-trip verifier for environments without pytest.

Usage:
    python verify_roundtrip.py
"""
from __future__ import annotations
import os
import sys
import tempfile
import pathlib
import base64
from typing import Any, Dict, List, Tuple

from db_json_bridge import dump_db_to_json, restore_db_from_json
from connect_database import connect_database


def _list_user_tables(cur) -> List[str]:
    cur.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    return [r[0] for r in cur.fetchall()]


def _list_columns(cur, table: str) -> List[str]:
    cur.execute(f"PRAGMA table_info({table})")
    return [r[1] for r in cur.fetchall()]


def _normalize_value(v: Any) -> Any:
    if isinstance(v, memoryview):
        v = bytes(v)
    if isinstance(v, (bytes, bytearray)):
        return {"__blob__": True, "base64": base64.b64encode(bytes(v)).decode("ascii")}
    return v


def _fetch_table(cur, table: str) -> Tuple[List[str], List[Tuple[Any, ...]]]:
    cols = _list_columns(cur, table)
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    return cols, rows


def _rows_as_normalized_dicts(cols: List[str], rows: List[Tuple[Any, ...]]) -> List[Dict[str, Any]]:
    return [{c: _normalize_value(v) for c, v in zip(cols, r)} for r in rows]


def _sorted_rows(rows: List[Dict[str, Any]], key_cols: List[str]) -> List[Dict[str, Any]]:
    if not rows:
        return rows
    if not key_cols:
        key_cols = [next(iter(rows[0].keys()))]

    def sort_key(d):
        return tuple(str(d.get(k)) for k in key_cols)

    return sorted(rows, key=sort_key)


def main():
    db_name_file = pathlib.Path("db_name.txt")
    if not db_name_file.exists():
        print("ERROR: db_name.txt not found; create it with your .db path.")
        sys.exit(2)
    original_db = db_name_file.read_text().strip()
    if not os.path.exists(original_db):
        print(f"ERROR: Original DB not found: {original_db}")
        sys.exit(2)

    with tempfile.TemporaryDirectory() as td:
        out_json = os.path.join(td, "dump.json")
        restored_db = os.path.join(td, "restored.db")

        print(f"→ Dumping {original_db} → {out_json}")
        dump_db_to_json(original_db, out_json)

        print(f"→ Restoring {out_json} → {restored_db}")
        restore_db_from_json(restored_db, out_json, overwrite=True)

        print("→ Comparing tables, columns, and rows …")
        with connect_database(original_db) as orig, connect_database(restored_db) as rest:
            orig_tables = _list_user_tables(orig.cursor)
            rest_tables = _list_user_tables(rest.cursor)
            if orig_tables != rest_tables:
                raise SystemExit(f"Tables differ.\nOrig: {orig_tables}\nRest: {rest_tables}")

            for t in orig_tables:
                o_cols, o_rows = _fetch_table(orig.cursor, t)
                r_cols, r_rows = _fetch_table(rest.cursor, t)
                if o_cols != r_cols:
                    raise SystemExit(f"Columns differ for table {t}.\nOrig: {o_cols}\nRest: {r_cols}")

                id_like = [c for c in o_cols if c.endswith("_id") or c == "id"]
                o_norm = _sorted_rows(_rows_as_normalized_dicts(o_cols, o_rows), id_like)
                r_norm = _sorted_rows(_rows_as_normalized_dicts(r_cols, r_rows), id_like)
                if o_norm != r_norm:
                    raise SystemExit(f"Row mismatch in table '{t}'.")

        print("✅ Round-trip verification PASSED.")


def run_roundtrip_check() -> None:
    """Programmatic entry point used by the TUI."""
    main()


if __name__ == "__main__":
    main()
