# db_json_bridge.py
"""
Dump your SQLite DB to JSON (great for Git diffs) and restore it back.

- Keeps primary keys & FKs intact by inserting with explicit column lists.
- Base64 encodes BLOBs as {"__blob__": true, "base64": "..."}.
- Restore uses your canonical schema from create_tables.create_all_tables().
"""

from __future__ import annotations
import json, base64, os, datetime
from typing import Any, Dict, List

from connect_database import connect_database         # enforces PRAGMA foreign_keys=ON
from create_tables import create_tables               # canonical schema builder


# ---------- helpers ----------

def _list_user_tables(cursor) -> List[str]:
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    return [r[0] for r in cursor.fetchall()]

def _list_columns(cursor, table: str) -> List[str]:
    cursor.execute(f"PRAGMA table_info({table})")
    return [r[1] for r in cursor.fetchall()]

def _serialize_cell(v: Any) -> Any:
    if isinstance(v, (bytes, bytearray)):
        return {"__blob__": True, "base64": base64.b64encode(v).decode("ascii")}
    return v

def _deserialize_cell(v: Any) -> Any:
    if isinstance(v, dict) and v.get("__blob__") and "base64" in v:
        return base64.b64decode(v["base64"].encode("ascii"))
    return v

def _insert_rows(cursor, table: str, columns: List[str], rows: List[Dict[str, Any]]):
    if not rows:
        return
    placeholders = ",".join(["?"] * len(columns))
    collist = ",".join(columns)
    sql = f"INSERT INTO {table} ({collist}) VALUES ({placeholders})"
    for row in rows:
        values = [_deserialize_cell(row.get(c)) for c in columns]
        cursor.execute(sql, values)


# ---------- export ----------

def dump_db_to_json(db_path: str, json_path: str) -> None:
    payload: Dict[str, Any] = {
        "meta": {
            "exported_at": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "source_db": os.path.basename(db_path),
        },
        "tables": {}
    }

    with connect_database(db_path) as db:
        for t in _list_user_tables(db.cursor):
            db.cursor.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (t,)
            )
            create_sql = (db.cursor.fetchone() or [None])[0]
            cols = _list_columns(db.cursor, t)
            db.cursor.execute(f"SELECT * FROM {t}")
            rows = db.cursor.fetchall()
            rows_as_dicts = [{c: _serialize_cell(v) for c, v in zip(cols, r)} for r in rows]
            payload["tables"][t] = {
                "create_sql": create_sql,   # informational
                "columns": cols,
                "rows": rows_as_dicts,
            }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Exported {db_path} → {json_path}")


# ---------- import (restore) ----------

# Safe dependency order for your schema (parents before children).
_BASE_ORDER = [
    "test_and_verification",
    "documents",
    "id_glossary",
    "quality_requirements",
    "item",
    "goals",
    "drone_swarm_requirements",
    "system_requirements",        # self-referential via parent_id
    "subsystem_requirements",     # self-referential via parent_id
    "V_join_documents",
    "sysreq_children",
    "sys_join_item",
    "goal_children",
    "swarm_req_children",
]

def _phase_insert_self_ref(cursor, table: str, cols: List[str],
                           rows: List[Dict[str, Any]], parent_col: str) -> None:
    # phase 1: roots (no parent)
    remaining = rows[:]
    phase1 = [r for r in remaining if r.get(parent_col) in (None, "")]
    _insert_rows(cursor, table, cols, phase1)
    remaining = [r for r in remaining if r not in phase1]

    if not remaining:
        return

    # phase 2+: resolve in passes once parents exist
    max_passes = 10
    for _ in range(max_passes):
        if not remaining:
            return
        cursor.execute(f"SELECT {cols[0]} FROM {table}")   # assumes first col is the id, matches your schema
        existing = {x[0] for x in cursor.fetchall()}
        ready, pending = [], []
        for r in remaining:
            p = r.get(parent_col)
            (ready if (p in (None, "") or p in existing) else pending).append(r)
        if ready:
            _insert_rows(cursor, table, cols, ready)
        if len(pending) == len(remaining):
            missing = sorted({r.get(parent_col) for r in pending})
            raise RuntimeError(f"Unresolved parents in {table}: {missing}")
        remaining = pending

def restore_db_from_json(db_path: str, json_path: str, overwrite: bool = False) -> None:
    if overwrite and os.path.exists(db_path):
        os.remove(db_path)

    with open(json_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    tables_content: Dict[str, Dict[str, Any]] = payload.get("tables", {})

    with connect_database(db_path) as db:
        # canonical schema from code
        create_tables(db.cursor).create_all_tables()

        present = [t for t in _BASE_ORDER if t in tables_content]
        extras = [t for t in tables_content.keys() if t not in present]
        ordered = present + extras

        for t in ordered:
            info = tables_content[t]
            cols = info["columns"]
            rows = info["rows"]

            if t == "system_requirements" and "parent_id" in cols:
                _phase_insert_self_ref(db.cursor, t, cols, rows, parent_col="parent_id")
            elif t == "subsystem_requirements" and "parent_id" in cols:
                _phase_insert_self_ref(db.cursor, t, cols, rows, parent_col="parent_id")
            else:
                _insert_rows(db.cursor, t, cols, rows)

    print(f"Restored {db_path} from {json_path} (overwrite={overwrite})")


# ---------- CLI ----------

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="SQLite DB ⇄ JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("dump", help="Dump .db → .json")
    d.add_argument("db")
    d.add_argument("json")

    r = sub.add_parser("restore", help="Restore .json → .db")
    r.add_argument("json")
    r.add_argument("db")
    r.add_argument("--overwrite", action="store_true")

    a = p.parse_args()
    if a.cmd == "dump":
        dump_db_to_json(a.db, a.json)
    else:
        restore_db_from_json(a.db, a.json, overwrite=a.overwrite)
