# tests/test_db_json_roundtrip.py
"""
End-to-end test:
1) Dump original DB -> JSON
2) Restore JSON -> temp DB
3) Assert same user tables, same columns, same row contents (order-agnostic)

Run:
    pytest -q
"""

from __future__ import annotations
import os
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
    # Make values comparable & sortable
    if isinstance(v, memoryview):
        v = bytes(v)
    if isinstance(v, (bytes, bytearray)):
        # base64 so it’s JSON-safe & sortable deterministically
        return {"__blob__": True, "base64": base64.b64encode(bytes(v)).decode("ascii")}
    return v


def _fetch_table(cur, table: str) -> Tuple[List[str], List[Tuple[Any, ...]]]:
    cols = _list_columns(cur, table)
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    return cols, rows


def _rows_as_normalized_dicts(cols: List[str], rows: List[Tuple[Any, ...]]) -> List[Dict[str, Any]]:
    out = []
    for r in rows:
        d = {c: _normalize_value(v) for c, v in zip(cols, r)}
        out.append(d)
    return out


def _sorted_rows(rows: List[Dict[str, Any]], key_cols: List[str]) -> List[Dict[str, Any]]:
    # Sort rows deterministically by key_cols (fallback to all columns if empty)
    if not rows:
        return rows
    if not key_cols:
        # assume first column is ID as in your schema
        key_cols = [next(iter(rows[0].keys()))]

    def sort_key(d):
        return tuple(str(d.get(k)) for k in key_cols)

    return sorted(rows, key=sort_key)


def test_roundtrip_equivalence(tmp_path: pathlib.Path):
    # Resolve original DB (project keeps active db path in db_name.txt)
    db_name_file = pathlib.Path("db_name.txt")
    assert db_name_file.exists(), "db_name.txt not found; create it with your .db path."
    original_db = db_name_file.read_text().strip()
    assert os.path.exists(original_db), f"Original DB not found at: {original_db}"

    out_json = tmp_path / "dump.json"
    restored_db = tmp_path / "restored.db"

    # 1) Dump
    dump_db_to_json(original_db, str(out_json))

    # 2) Restore
    restore_db_from_json(str(restored_db), str(out_json), overwrite=True)

    # 3) Compare
    with connect_database(original_db) as orig, connect_database(str(restored_db)) as rest:
        orig_tables = _list_user_tables(orig.cursor)
        rest_tables = _list_user_tables(rest.cursor)
        assert orig_tables == rest_tables, f"Tables differ.\nOrig: {orig_tables}\nRest: {rest_tables}"

        for t in orig_tables:
            o_cols, o_rows = _fetch_table(orig.cursor, t)
            r_cols, r_rows = _fetch_table(rest.cursor, t)
            assert o_cols == r_cols, f"Columns differ for table {t}.\nOrig: {o_cols}\nRest: {r_cols}"

            o_norm = _rows_as_normalized_dicts(o_cols, o_rows)
            r_norm = _rows_as_normalized_dicts(r_cols, r_rows)

            # Choose a stable sort key: if table has an obvious id column, use that
            id_like = [c for c in o_cols if c.endswith("_id") or c == "id"]
            o_sorted = _sorted_rows(o_norm, id_like)
            r_sorted = _sorted_rows(r_norm, id_like)
            assert o_sorted == r_sorted, f"Row mismatch in table '{t}'."
